from datetime import datetime

from pydantic import BaseModel

from app.models.embedded.geo_json import *
from app.models.embedded.enums import DisasterAreaStatus


class DisasterAreaCreateReq(BaseModel):
    title: str
    description: str
    boundary: GeoJSONPolygon


class DisasterAreaCreateRes(BaseModel):
    creator_uid: str
    title: str
    description: str
    boundary: GeoJSONPolygon
    marks: List[GeoJSONPolygon | GeoJSONLineString | GeoJSONPoint]
    status: DisasterAreaStatus
    created_at: datetime
    updated_at: datetime
    resolved_at: Optional[datetime] = None