from datetime import datetime
from typing import Annotated, List, Optional

import pymongo
from beanie import Document, Indexed

from app.models.embedded.enums import DisasterAreaStatus
from app.models.embedded.geo_json import GeoJSONLineString, GeoJSONPoint, GeoJSONPolygon


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
