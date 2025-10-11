from typing import Annotated

from beanie import Indexed, PydanticObjectId
from pydantic import BaseModel

from app.models.general.geo_json import GeoJSONPolygon


class TileAreaUpdateDTO(BaseModel):
    area: GeoJSONPolygon
    area_id: Annotated[PydanticObjectId, Indexed()]
    spacing_m: int = 200
    update_interval_seconds: int = 300
