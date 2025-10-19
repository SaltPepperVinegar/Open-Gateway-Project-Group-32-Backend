from datetime import datetime
from typing import Optional

from beanie import Document

from app.models.embedded.geo_json import GeoJSONPoint
from app.models.embedded.enums import SurvivorReportEmergencyLevel


class SurvivorReportDocument(Document):
    title: Optional[str]
    description: Optional[str]
    level: Optional[SurvivorReportEmergencyLevel]
    location: GeoJSONPoint
    address: Optional[str]
    created_at: datetime

    class Settings:
        name = "survivor_reports"