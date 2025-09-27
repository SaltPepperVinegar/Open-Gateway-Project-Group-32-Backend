from datetime import datetime, timezone
from typing import Annotated, Literal

from beanie import Document, Indexed, PydanticObjectId
from pydantic import Field

from app.models.general.geo_json import GeoJSONPolygon


class TilingAreaDoc(Document):
    area_id: Annotated[PydanticObjectId, Indexed()]

    tiling_version: int

    area: GeoJSONPolygon
    spacing_m: int

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    status: Literal["active", "stale"] = "active"

    class Settings:
        name = "tiling_areas"
