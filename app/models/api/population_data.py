from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.models.general.geo_json import GeoJSONPolygon


class PopulationWindowIn(BaseModel):
    # [min_lon, min_lat, max_lon, max_lat]
    bbox: list[float] = Field(..., min_items=4, max_items=4)
    time_from: Optional[datetime] = None
    time_to: Optional[datetime] = None


class AreaPopulationOut(BaseModel):
    area: GeoJSONPolygon
    population: float
