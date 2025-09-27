from datetime import datetime, timezone

from app.models.db.tile import TileDoc
from app.models.db.tile_area import TilingAreaDoc
from app.models.db.tiling_job import TilingJobDoc
from app.repository.tile_batch_process import process_tile_batch
from app.repository.tiling_service import build_tiles_and_store


async def run_tiling_job(job: TilingJobDoc):
    try:
        job.status = "running"
        await job.save()

        # 2) process in batches
        processed_total = 0
        while True:
            processed = await process_tile_batch(job, batch_size=200, concurrency=16)
            if processed == 0:
                break
            processed_total += processed
            job.processed_tiles = processed_total
            job.updated_at = datetime.now(timezone.utc)
            await job.save()

        job.status = "completed"
        job.updated_at = datetime.now(timezone.utc)

        await TileDoc.find(
            {
                "area_id": job.area_id,
                "tiling_version": {"$lte": job.tiling_version},
                "tiling_epoch": {"$lt": job.tiling_epoch},
                "status": {"$in": ["pending", "processing", "ready", "failed"]},
            }
        ).update_many(
            {
                "$set": {
                    "status": "stale",
                    "updated_at": datetime.now(timezone.utc),
                }
            }
        )
        await job.save()
    except Exception as e:
        job.status = "failed"
        job.error = str(e)
        job.updated_at = datetime.now(timezone.utc)
        await job.save()
        raise


async def create_tiling_job(area: TilingAreaDoc) -> TilingJobDoc:

    job = TilingJobDoc(
        area_id=area.area_id,
        tiling_version=area.tiling_version,
        tiling_epoch=datetime.now(timezone.utc),
    )

    await job.insert()

    inserted = await build_tiles_and_store(area, job)
    job.total_tiles = inserted
    await job.save()

    return job
