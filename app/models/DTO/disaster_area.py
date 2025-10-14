from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, Field

from app.models.embedded.enums import DisasterAreaStatus
from app.models.embedded.geo_json import GeoJSONPolygon


class DisasterAreaCreateDTO(BaseModel):
    creator_uid: str
    title: str
    description: str
    boundary: GeoJSONPolygon
    status: DisasterAreaStatus = DisasterAreaStatus.ACTIVE
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    resolved_at: Optional[datetime] = None
