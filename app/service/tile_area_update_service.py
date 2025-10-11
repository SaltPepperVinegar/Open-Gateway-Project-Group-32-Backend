from app.models.DTO.tile import TileAreaUpdateDTO
from app.repository.tile.tile_area_update import update_tile_area
from app.repository.tile.tiling_job_create import create_tiling_job


async def update_tile_area_service(update: TileAreaUpdateDTO):

    area = await update_tile_area(update)
    await create_tiling_job(area, priority=1)
