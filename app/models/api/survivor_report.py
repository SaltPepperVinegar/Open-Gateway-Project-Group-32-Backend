from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.models.embedded.enums import SurvivorReportEmergencyLevel
from app.models.embedded.geo_json import GeoJSONPoint


class SurvivorReportCreateReq(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    level: Optional[SurvivorReportEmergencyLevel] = None
    location: GeoJSONPoint
    address: Optional[str] = None


class SurvivorReportCreateRes(BaseModel):
    id: str  # String representing MongoDB ObjectID
    title: Optional[str]
    description: Optional[str]
    level: Optional[SurvivorReportEmergencyLevel]
    location: GeoJSONPoint
    address: Optional[str]
    created_at: datetime


class SurvivorReportRetrieveRes(BaseModel):
    id: str  # String representing MongoDB ObjectID
    title: Optional[str]
    description: Optional[str]
    level: Optional[SurvivorReportEmergencyLevel]
    location: GeoJSONPoint
    address: Optional[str]
    created_at: datetime
