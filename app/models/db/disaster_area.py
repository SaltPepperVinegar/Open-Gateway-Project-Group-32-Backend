from datetime import datetime, timezone
from typing import Optional, Annotated

from beanie import Document, Indexed
import pymongo

from app.models.embedded.geo_json import *
from app.models.embedded.enums import DisasterAreaStatus


class DisasterAreaDocument(Document):
    creator_uid: str
    title: str
    description: str
    boundary: Annotated[GeoJSONPolygon, Indexed(index_type=pymongo.GEOSPHERE)]
    marks: List[GeoJSONPolygon | GeoJSONLineString | GeoJSONPoint]
    status: DisasterAreaStatus
    created_at: datetime
    updated_at: datetime
    resolved_at: Optional[datetime] = None

    class Settings:
        name = "disaster_areas"
