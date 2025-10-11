from datetime import datetime, timezone

from app.models.db.tile_area import TilingAreaDoc
from app.models.db.tiling_job import TilingJobDoc
from app.repository.tile.tile_build import build_tiles_and_store


async def create_tiling_job(area: TilingAreaDoc, priority=0) -> TilingJobDoc:
    area.schedule_next_update()
    await area.save()

    job = TilingJobDoc(
        area_id=area.area_id,
        tiling_version=area.tiling_version,
        tiling_epoch=datetime.now(timezone.utc),
        priority=priority,
    )
    print(
        f"creating tile job {job.area_id}, version: {job.tiling_version}, epoch: {job.tiling_epoch}"
    )

    inserted = await build_tiles_and_store(area, job)
    job.total_tiles = inserted
    await job.insert()

    return job
