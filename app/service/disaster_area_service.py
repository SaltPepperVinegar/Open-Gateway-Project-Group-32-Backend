from typing import Dict, Any

from fastapi import HTTPException, status

from app.models.api.disaster_area import DisasterAreaCreateReq, DisasterAreaCreateRes
from app.models.embedded.enums import UserRole
from app.models.DTO.disaster_area import DisasterAreaCreateDTO
from app.repository.disaster_area_repo import create_disaster_area


async def create_disaster_area_service(
        req: DisasterAreaCreateReq, decoded_token: Dict[str, Any]
) -> DisasterAreaCreateRes:
    if "role" not in decoded_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing 'role' in token claims."
        )

    if decoded_token["role"] != UserRole.MANAGER.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only managers can create a new disaster area."
        )
    
    disaster_area_dto = DisasterAreaCreateDTO(
        creator_uid=decoded_token["uid"],
        title=req.title,
        description=req.description,
        boundary=req.boundary
    )

    created_disaster_area = await create_disaster_area(disaster_area_dto)

    return DisasterAreaCreateRes(**created_disaster_area.model_dump())

