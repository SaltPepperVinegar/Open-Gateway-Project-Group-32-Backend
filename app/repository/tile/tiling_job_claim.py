from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from beanie import PydanticObjectId
from pymongo import ASCENDING, DESCENDING, ReturnDocument

from app.models.db.tiling_job import TilingJobDoc


async def claim_next_job() -> Optional[TilingJobDoc]:
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
    return TilingJobDoc.get_pymongo_collection()


async def heartbeat(job_id: PydanticObjectId, *, interval_s: float) -> None:
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


async def update_progress(
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


async def mark_completed(job_id: PydanticObjectId) -> None:
    coll = _jobs_coll()
    now = _now()
    await coll.update_one(
        {"_id": job_id},
        {"$set": {"status": "completed", "updated_at": now}},
    )


async def mark_failed(job_id: PydanticObjectId, message: str) -> None:
    coll = _jobs_coll()
    now = _now()
    await coll.update_one(
        {"_id": job_id},
        {"$set": {"status": "failed", "error": message, "updated_at": now}},
    )


async def mark_canceled(job_id: PydanticObjectId, note: str = "") -> None:
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
