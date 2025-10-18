from typing import Annotated, Any, Dict, List

from fastapi import APIRouter, Depends

from app.api.v1.users_depends import get_decoded_token
from app.models.api.disaster_area import DisasterAreaCreateReq, DisasterAreaCreateRes, DisasterAreaSearchRes, DisasterAreaSearchQueryParam
from app.service.disaster_area_service import create_disaster_area_service, search_disaster_areas_service

router = APIRouter(prefix="/disaster_areas", tags=["disaster_areas"])


@router.post("", response_model=DisasterAreaCreateRes, status_code=201)
async def create_disaster_area(
    req: DisasterAreaCreateReq,
    decoded_token: Annotated[Dict[str, Any], Depends(get_decoded_token)],
) -> DisasterAreaCreateRes:
    return await create_disaster_area_service(req, decoded_token)


@router.get("", response_model=List[DisasterAreaSearchRes], status_code=200)
async def search_disaster_areas(
    query: DisasterAreaSearchQueryParam = Depends()
) -> List[DisasterAreaSearchRes]:
    return await search_disaster_areas_service(query)