from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.models.general.geo_json import GeoJSONPolygon


class PopulationWindowIn(BaseModel):
    # [min_lon, min_lat, max_lon, max_lat]
    area: GeoJSONPolygon
    time_from: Optional[datetime] = None
    time_to: Optional[datetime] = None
