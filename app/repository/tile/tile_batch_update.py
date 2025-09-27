import asyncio
import random
from datetime import datetime, timezone

from fastapi import HTTPException

from app.exceptions.tile_batch_exceptions import TileBatchError
from app.models.db.tile import TileDoc
from app.models.db.tiling_job import TilingJobDoc
from app.models.general.geo_json import GeoJSONPolygon


async def process_tile_job(
    job: TilingJobDoc,
    batch_size=100,
    tile_concurrency=10,
    heartbeat_s=10,
):
    print(f"processing {job.area_id}, {job.tiling_version}, {job.tiling_epoch}")
    try:
        job.status = "running"
        await job.save()

        # 2) process in batches
        processed_total = 0
        while True:
            processed = await process_tile_batch(
                job, batch_size=batch_size, concurrency=tile_concurrency
            )
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
    except (TileBatchError, HTTPException) as e:
        job.status = "failed"
        job.error = str(e)
        job.updated_at = datetime.now(timezone.utc)
        await job.save()
        raise


async def process_tile_batch(job: TilingJobDoc, batch_size=100, concurrency=10):
    # Pull a batch of pending tiles for this version
    tiles = (
        await TileDoc.find(
            TileDoc.area_id == job.area_id,
            TileDoc.tiling_version == job.tiling_version,
            TileDoc.tiling_epoch == job.tiling_epoch,
            TileDoc.status == "pending",
        )
        .limit(batch_size)
        .to_list()
    )
    if not tiles:
        return 0

    ids = [t.id for t in tiles]
    await TileDoc.find({"_id": {"$in": ids}}).update_many(
        {"$set": {"status": "processing"}}
    )

    sem = asyncio.Semaphore(concurrency)

    async def _work(t: TileDoc):
        async with sem:
            try:
                metrics = await get_population_density(t.boundary)
                await t.update(
                    {
                        "$set": {
                            "metrics": metrics,
                            "metrics_updated_at": datetime.now(timezone.utc),
                            "status": "ready",
                            "updated_at": datetime.now(timezone.utc),
                        }
                    }
                )
            except (HTTPException, asyncio.TimeoutError) as e:
                await t.update(
                    {
                        "$set": {
                            "status": "failed",
                            "last_error": str(e),
                            "updated_at": datetime.now(timezone.utc),
                        }
                    }
                )
                raise TileBatchError from e

    await asyncio.gather(*[_work(t) for t in tiles])
    return len(tiles)


async def get_population_density(area: GeoJSONPolygon):
    return random.randint(100, 200)
