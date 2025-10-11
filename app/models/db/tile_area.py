from datetime import datetime, timedelta, timezone
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
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    update_interval_seconds: int = 300
    next_update_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def schedule_next_update(self):
        now = datetime.now(timezone.utc)
        next_at = self.next_update_at
        interval = timedelta(seconds=self.update_interval_seconds)
        while next_at <= now:
            next_at += interval
        self.next_update_at = next_at

    status: Literal["active", "stale", "pause"] = "active"

    class Settings:
        name = "tiling_areas"
