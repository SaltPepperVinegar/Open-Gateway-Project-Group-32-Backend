from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.models.embedded.enums import DisasterAreaStatus
from app.models.embedded.geo_json import (
    GeoJSONPolygon,
)


class DisasterAreaCreateReq(BaseModel):
    title: str
    description: str
    boundary: GeoJSONPolygon


class DisasterAreaCreateRes(BaseModel):
    creator_uid: str
    title: str
    description: str
    boundary: GeoJSONPolygon
    status: DisasterAreaStatus
    created_at: datetime
    updated_at: datetime
    resolved_at: Optional[datetime] = None
