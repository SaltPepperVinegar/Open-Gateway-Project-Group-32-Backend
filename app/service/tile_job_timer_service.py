import asyncio

from app.repository.tile.tiling_area import claim_one_area_need_location_update
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
            area = await claim_one_area_need_location_update()
            if not area:
                await asyncio.sleep(poll_interval_s)
                continue
            await create_tiling_job(area)

    except asyncio.CancelledError:
        print("[tile_area_update_loop] Cancelled, shutting down gracefully.")
        raise
