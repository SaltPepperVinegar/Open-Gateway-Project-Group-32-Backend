import asyncio
from datetime import datetime, timedelta, timezone
from typing import Optional

from pymongo import ReturnDocument

from app.models.db.tile_area import TilingAreaDoc
from app.repository.tile.tiling_job_create import create_tiling_job


async def tile_area_update_loop(
    poll_interval_s: float = 2.0,
) -> None:
    """
    Infinite loop: claim next job and process it.
    Call this in a long-running task (e.g., inside your app lifespan or a dedicated worker).
    """
    try:
        while True:
            area = await claim_one_due_area()
            if not area:
                await asyncio.sleep(poll_interval_s)
                continue
            await create_tiling_job(area)
            area.schedule_next_update()
            await area.save()

    except asyncio.CancelledError:
        print("[tile_area_update_loop] Cancelled, shutting down gracefully.")
        raise


async def claim_one_due_area(
    lock_hold: timedelta = timedelta(minutes=5),
) -> Optional[TilingAreaDoc]:
    """
    Atomically 'claim' a single due area by pushing its next_update_at forward briefly
    (lock_hold) so other schedulers won't pick it up at the same time.
    Returns the claimed area (as a TilingAreaDoc), or None if none available.
    """
    col = TilingAreaDoc.get_pymongo_collection()
    now = datetime.now(timezone.utc)
    claimed_raw = await col.find_one_and_update(
        {
            "status": "active",
            "next_update_at": {"$lte": now},
        },
        {"$set": {"next_update_at": now + lock_hold}},
        return_document=ReturnDocument.BEFORE,
        sort=[("next_update_at", 1)],
    )

    if not claimed_raw:
        return None
    return TilingAreaDoc.model_validate(claimed_raw)
