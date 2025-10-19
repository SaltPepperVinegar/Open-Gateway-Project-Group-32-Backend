from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, Field

from app.models.embedded.enums import SurvivorReportEmergencyLevel
from app.models.embedded.geo_json import GeoJSONPoint


class SurvivorReportDTO(BaseModel):
    id: str  # String representing MongoDB ObjectID
    title: Optional[str]
    description: Optional[str]
    level: Optional[SurvivorReportEmergencyLevel]
    location: GeoJSONPoint
    address: Optional[str]
    created_at: datetime


class SurvivorReportCreateDTO(BaseModel):
    title: Optional[str]
    description: Optional[str]
    level: Optional[SurvivorReportEmergencyLevel]
    location: GeoJSONPoint
    address: Optional[str]
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
