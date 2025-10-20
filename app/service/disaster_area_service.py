from typing import Any, Dict, List

from beanie import PydanticObjectId
from fastapi import HTTPException, status

from app.core.config import settings
from app.exceptions.disaster_area import WorkerCreatesDisasterAreaError
from app.exceptions.general import InvalidObjectIDStringError
from app.models.api.disaster_area import (
    DisasterAreaCreateReq,
    DisasterAreaCreateRes,
    DisasterAreaSearchQueryParam,
    DisasterAreaSearchRes,
    DisasterAreaUpdateReq,
    DisasterAreaUpdateRes,
)
from app.models.DTO.disaster_area import DisasterAreaCreateDTO, DisasterAreaUpdateDTO
from app.models.DTO.tile import TileAreaRemoveDTO, TileAreaUpdateDTO
from app.models.embedded.enums import DisasterAreaStatus, UserRole
from app.models.general.geo_json import GeoJSONPolygon as GeoJSONPolygonTile
from app.repository.disaster_area_repo import (
    create_disaster_area,
    search_disaster_area,
    update_disaster_area,
)
from app.service.tile_area_update_service import (
    remove_tile_area,
    update_tile_area_service,
)


async def create_disaster_area_service(
    req: DisasterAreaCreateReq, decoded_token: Dict[str, Any]
) -> DisasterAreaCreateRes:
    if "role" not in decoded_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing 'role' in token claims.",
        )

    if decoded_token["role"] != UserRole.MANAGER.value:
        raise WorkerCreatesDisasterAreaError()

    disaster_area_dto = DisasterAreaCreateDTO(
        creator_uid=decoded_token["uid"],
        title=req.title,
        description=req.description,
        boundary=req.boundary,
    )

    created_disaster_area = await create_disaster_area(disaster_area_dto)

    # Create tile update job for the new disaster area

    await update_tile_area_service(
        TileAreaUpdateDTO(
            area=GeoJSONPolygonTile(
                type=created_disaster_area.boundary.type,
                coordinates=created_disaster_area.boundary.coordinates,
            ),
            area_id=PydanticObjectId(created_disaster_area.id),
            spacing_m=settings.SPACING_M,
        )
    )

    return DisasterAreaCreateRes(**created_disaster_area.model_dump())


async def search_disaster_areas_service(
    query: DisasterAreaSearchQueryParam,
) -> List[DisasterAreaSearchRes]:
    results = await search_disaster_area(query.status)

    return [DisasterAreaSearchRes(**result.model_dump()) for result in results]


async def update_disaster_area_service(
    id: str, update_info: DisasterAreaUpdateReq
) -> DisasterAreaUpdateRes:
    try:
        update_dto = DisasterAreaUpdateDTO(id=id, status=update_info.status)
    except ValueError:
        raise InvalidObjectIDStringError() from ValueError

    disaster_area_dto = await update_disaster_area(update_dto)

    # Update tile job according to status

    if (
        update_info.status == DisasterAreaStatus.RESOLVED
        or update_info.status == DisasterAreaStatus.DELETED
    ):
        # If new status is resolved or deleted, remove corresponding tile job
        await remove_tile_area(
            TileAreaRemoveDTO(area_id=PydanticObjectId(disaster_area_dto.id))
        )
    else:
        # If new status is active, create tile job
        await update_tile_area_service(
            TileAreaUpdateDTO(
                area=GeoJSONPolygonTile(
                    type=disaster_area_dto.boundary.type,
                    coordinates=disaster_area_dto.boundary.coordinates,
                ),
                area_id=PydanticObjectId(disaster_area_dto.id),
            )
        )

    return DisasterAreaUpdateRes(**disaster_area_dto.model_dump())
