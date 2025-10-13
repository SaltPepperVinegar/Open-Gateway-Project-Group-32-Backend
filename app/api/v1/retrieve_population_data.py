from typing import Annotated, Any, Dict, List

from fastapi import APIRouter, Depends

from app.api.v1.users_depends import get_decoded_token
from app.models.api.population_data import PopulationWindowIn
from app.service.population_window_service import retrieve_population_data

router = APIRouter(prefix="/population_data", tags=["population_data"])


@router.post("", response_model=List[List[float]], status_code=201)
async def retrieve_population_data_of_window(
    req: PopulationWindowIn,
    decoded_token: Annotated[Dict[str, Any], Depends(get_decoded_token)],
) -> List[List[float]]:
    return await retrieve_population_data(req)
