from __future__ import annotations

import asyncio

from app.repository.tile.tiling_job_claim import claim_next_job, mark_failed
from app.repository.tile.tiling_job_process import process_tile_job


async def tile_queue_loop(
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
        job = await claim_next_job()
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
            await mark_failed(job.id, "Worker task cancelled")
            raise
        except Exception as e:
            await mark_failed(job.id, f"Unhandled worker error: {e!r}")
