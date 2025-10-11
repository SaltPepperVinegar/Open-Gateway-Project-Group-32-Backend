from typing import List

from fastapi import APIRouter

from app.models.api.population_data import AreaPopulationOut, PopulationWindowIn
from app.service.population_window_service import retrieve_population_data

router = APIRouter(prefix="/population_data", tags=["population_data"])


@router.post("", response_model=List[AreaPopulationOut], status_code=201)
async def retrieve_population_data_of_window(
    req: PopulationWindowIn,
) -> List[AreaPopulationOut]:
    return await retrieve_population_data(req)
