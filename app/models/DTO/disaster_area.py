from typing import Optional
from datetime import datetime, timezone

from pydantic import BaseModel, Field

from app.models.embedded.geo_json import *
from app.models.embedded.enums import DisasterAreaStatus

class DisasterAreaCreateDTO(BaseModel):
    creator_uid: str
    title: str
    description: str
    boundary: GeoJSONPolygon
    marks: List[GeoJSONPolygon | GeoJSONLineString | GeoJSONPoint] = []
    status: DisasterAreaStatus = DisasterAreaStatus.ACTIVE
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    resolved_at: Optional[datetime] = None