from datetime import datetime
from typing import Optional

from beanie import Document
from bson import ObjectId
from pydantic import Field
from pymongo import GEOSPHERE, IndexModel

from app.models.general import GeoJSONPolygon


class DisasterArea(Document):
    creator_id: ObjectId = Field(..., description="Manager user who created this disaster area")
    title: str
    description: str
    boundary: GeoJSONPolygon = Field(..., description="GeoJSON Polygon")
    is_resolved: bool = False
    created_at: datetime = Field(default_factory=datetime.now(datetime.timezone.utc))
    resolved_at: Optional[datetime] = None

    class Settings:
        name = "disaster_areas"
        indexes = [
            IndexModel([("boundary", GEOSPHERE)]),
        ]

    class Config:
        json_encoders = {ObjectId: str}
