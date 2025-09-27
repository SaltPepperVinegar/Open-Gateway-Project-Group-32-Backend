# app/repository/tiling_queue.py
from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from beanie import PydanticObjectId
from pymongo import ASCENDING, DESCENDING, ReturnDocument

from app.models.db.tiling_job import TilingJobDoc
from app.repository.tile.tile_batch_update import process_tile_job


async def worker_loop(
    *,
    poll_interval_s: float = 2.0,
    batch_size: int = 200,
    tile_concurrency: int = 10,
    heartbeat_s: float = 10.0,
) -> None:
    """
    Infinite loop: claim next job and process it.
    Call this in a long-running task (e.g., inside your app lifespan or a dedicated worker).
    """
    while True:
        job = await _claim_next_job()
        if not job:
            await asyncio.sleep(poll_interval_s)
            continue

        try:
            await process_tile_job(
                job,
                batch_size=batch_size,
                tile_concurrency=tile_concurrency,
                heartbeat_s=heartbeat_s,
            )
        except asyncio.CancelledError:
            await _mark_failed(job.id, "Worker task cancelled")
            raise
        except Exception as e:
            await _mark_failed(job.id, f"Unhandled worker error: {e!r}")


# ---------- Atomic claim / Heartbeat / Status helpers ----------


async def _claim_next_job() -> Optional[TilingJobDoc]:
    """
    Atomically claim the highest priority queued job (FIFO within same priority).
    Uses Motor to guarantee atomic findOneAndUpdate.
    """
    coll = _jobs_coll()

    now = _now()
    doc = await coll.find_one_and_update(
        {"status": "queued"},
        {
            "$set": {
                "status": "running",
                "updated_at": now,
            }
        },
        sort=[("priority", DESCENDING), ("created_at", ASCENDING)],
        return_document=ReturnDocument.AFTER,
    )

    return TilingJobDoc.model_validate(doc) if doc else None


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _jobs_coll() -> Any:
    # Beanie 2.x returns PyMongo async collection
    return TilingJobDoc.get_pymongo_collection()


async def _heartbeat(job_id: PydanticObjectId, *, interval_s: float) -> None:
    """
    Periodically touches 'updated_at' for a running job.
    Stops cleanly on task cancellation.
    """
    coll = _jobs_coll()
    try:
        while True:
            await asyncio.sleep(interval_s)
            await coll.update_one(
                {"_id": job_id, "status": "running"},
                {"$set": {"updated_at": _now()}},
            )
    except asyncio.CancelledError:
        # exit quietly — the worker loop decides how to mark job status
        raise


async def _update_progress(
    job_id: PydanticObjectId,
    *,
    inc_processed: int = 0,
    total_tiles: Optional[int] = None,
) -> None:
    """
    Increment processed count and/or set total tiles.
    Always refreshes updated_at.
    """
    coll = _jobs_coll()

    update: Dict[str, Any] = {"$set": {"updated_at": _now()}}
    if total_tiles is not None:
        update["$set"]["total_tiles"] = total_tiles
    if inc_processed:
        update["$inc"] = {"processed_tiles": inc_processed}

    await coll.update_one(
        {"_id": job_id},
        update,
    )


async def _mark_completed(job_id: PydanticObjectId) -> None:
    coll = _jobs_coll()
    now = _now()
    await coll.update_one(
        {"_id": job_id},
        {"$set": {"status": "completed", "updated_at": now}},
    )


async def _mark_failed(job_id: PydanticObjectId, message: str) -> None:
    coll = _jobs_coll()
    now = _now()
    await coll.update_one(
        {"_id": job_id},
        {"$set": {"status": "failed", "error": message, "updated_at": now}},
    )


async def _mark_canceled(job_id: PydanticObjectId, note: str = "") -> None:
    coll = _jobs_coll()
    now = _now()
    await coll.update_one(
        {"_id": job_id},
        {
            "$set": {
                "status": "canceled",
                "error": note or "Canceled",
                "updated_at": now,
            }
        },
    )


# ---------- Utilities ----------


@asynccontextmanager
async def contextlib_suppress(*exceptions):
    """
    Minimal async-friendly suppressor (since contextlib.suppress is sync-only in 3.11).
    """
    try:
        yield
    except exceptions:
        return


async def cancel_job(job_id: PydanticObjectId) -> bool:
    """
    Request cancel:
    - If queued: mark canceled immediately.
    - If running: mark canceled; worker will observe and stop between batches.
    Returns True if a doc was modified.
    """
    now = _now()
    res = await TilingJobDoc.get_motor_collection().update_one(
        {
            "_id": job_id,
            "status": {"$in": ["queued", "running"]},
        },
        {
            "$set": {"status": "canceled", "updated_at": now},
        },
    )
    return res.modified_count > 0
