from typing import Any, Dict

from fastapi import APIRouter, Depends
from typing_extensions import Annotated

from app.api.v1.users_depends import get_decoded_token
from app.models.db.tiling_job import TilingJobDoc
from app.models.DTO.tile import TileAreaUpdateDTO
from app.repository.tile.tiling_area import update_tile_area
from app.repository.tile.tiling_job_create import create_tiling_job

router = APIRouter(prefix="/tiles", tags=["tiles"])


@router.post("", response_model=TilingJobDoc, status_code=201)
async def update_tile_area_service_test(
    update: TileAreaUpdateDTO,
    decoded_token: Annotated[Dict[str, Any], Depends(get_decoded_token)],
):

    area = await update_tile_area(update)

    job = await create_tiling_job(area, priority=1)

    return job
