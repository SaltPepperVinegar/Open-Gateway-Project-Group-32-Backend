from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.models.embedded.enums import DisasterAreaStatus
from app.models.embedded.geo_json import GeoJSONPolygon


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


class DisasterAreaSearchQueryParam(BaseModel):
    """
    This data model represents query parameters for GET endpoint of disaster area.
    If status is specified, then return a list of disaster areas with specified status.
    If status is left None, then return all disaster areas.
    """

    status: Optional[DisasterAreaStatus] = None


class DisasterAreaSearchRes(BaseModel):
    """
    This data model is used for response body of GET endpoint of disaster area.
    """

    creator_uid: str
    title: str
    description: str
    boundary: GeoJSONPolygon
    status: DisasterAreaStatus
    created_at: datetime
    updated_at: datetime
    resolved_at: Optional[datetime]