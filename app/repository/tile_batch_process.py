import asyncio
import random
from datetime import datetime, timezone

from app.models.db.tile import TileDoc
from app.models.db.tiling_job import TilingJobDoc
from app.models.general.geo_json import GeoJSONPolygon


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

    # mark as processing (optimistic)
    ids = [t.id for t in tiles]
    await TileDoc.find(TileDoc.id.in_(ids)).update_many(
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
            except Exception as e:
                await t.update.update(
                    {
                        "$set": {
                            "status": "failed",
                            "last_error": str(e),
                            "updated_at": datetime.now(timezone.utc),
                        }
                    }
                )

    await asyncio.gather(*[_work(t) for t in tiles])
    return len(tiles)


def get_population_density(area: GeoJSONPolygon):
    return random.randint(100, 200)
