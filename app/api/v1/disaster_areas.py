from typing import Annotated, Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.v1.disaster_areas_depends import disaster_area_search_query_params
from app.api.v1.users_depends import get_decoded_token
from app.exceptions.disaster_area import (
    DisasterAreaDoesNotExistError,
    WorkerCreatesDisasterAreaError,
)
from app.exceptions.general import InvalidObjectIDStringError
from app.models.api.disaster_area import (
    DisasterAreaCreateReq,
    DisasterAreaCreateRes,
    DisasterAreaSearchQueryParam,
    DisasterAreaSearchRes,
    DisasterAreaUpdateReq,
    DisasterAreaUpdateRes,
)
from app.service.disaster_area_service import (
    create_disaster_area_service,
    search_disaster_areas_service,
    update_disaster_area_service,
)

router = APIRouter(prefix="/disaster_areas", tags=["disaster_areas"])


@router.post("", response_model=DisasterAreaCreateRes, status_code=201)
async def create_disaster_area(
    req: DisasterAreaCreateReq,
    decoded_token: Annotated[Dict[str, Any], Depends(get_decoded_token)],
) -> DisasterAreaCreateRes:
    try:
        return await create_disaster_area_service(req, decoded_token)
    except WorkerCreatesDisasterAreaError as err:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=err.message,
        ) from err


@router.get("", response_model=List[DisasterAreaSearchRes], status_code=200)
async def search_disaster_areas(
    query: Annotated[
        DisasterAreaSearchQueryParam, Depends(disaster_area_search_query_params)
    ],
) -> List[DisasterAreaSearchRes]:
    return await search_disaster_areas_service(query)


@router.patch("/{id}", response_model=DisasterAreaUpdateRes, status_code=200)
async def update_disaster_area(
    id: str, update_info: DisasterAreaUpdateReq
) -> DisasterAreaUpdateRes:
    try:
        return await update_disaster_area_service(id, update_info)
    except DisasterAreaDoesNotExistError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=err.message,
        ) from err
    except InvalidObjectIDStringError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=err.message,
        ) from err
