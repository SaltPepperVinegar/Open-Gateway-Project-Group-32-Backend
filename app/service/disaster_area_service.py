from typing import Any, Dict, List

from fastapi import HTTPException, status

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
from app.models.embedded.enums import UserRole
from app.repository.disaster_area_repo import (
    create_disaster_area,
    search_disaster_area,
    update_disaster_area,
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

    return DisasterAreaUpdateRes(**disaster_area_dto.model_dump())
