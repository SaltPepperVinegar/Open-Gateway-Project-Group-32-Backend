from typing import Optional
from datetime import datetime

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
    title: Optional[str]
    description: Optional[str]
    level: Optional[SurvivorReportEmergencyLevel]
    location: GeoJSONPoint
    address: Optional[str]
    created_at: datetime


class SurvivorReportRetrieveRes(BaseModel):
    title: Optional[str]
    description: Optional[str]
    level: Optional[SurvivorReportEmergencyLevel]
    location: GeoJSONPoint
    address: Optional[str]
    created_at: datetime
