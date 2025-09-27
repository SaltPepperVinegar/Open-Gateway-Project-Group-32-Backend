from app.models.DTO.tile import TileAreaUpdateDTO
from app.repository.tiling_job_runner import create_tiling_job, run_tiling_job


async def update_tile_area(update: TileAreaUpdateDTO):

    area = await update_tile_area(update)

    job = await create_tiling_job(area)

    await run_tiling_job(job)
