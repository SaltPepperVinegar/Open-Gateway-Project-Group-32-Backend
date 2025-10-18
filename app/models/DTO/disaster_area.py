from datetime import datetime, timezone
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field, field_validator

from app.models.embedded.enums import DisasterAreaStatus
from app.models.embedded.geo_json import GeoJSONPolygon


class DisasterAreaDTO(BaseModel):
    id: str  # String ID converted from MongoDB ObjectID
    creator_uid: str
    title: str
    description: str
    boundary: GeoJSONPolygon
    status: DisasterAreaStatus
    created_at: datetime
    updated_at: datetime
    resolved_at: Optional[datetime]


class DisasterAreaCreateDTO(BaseModel):
    creator_uid: str
    title: str
    description: str
    boundary: GeoJSONPolygon
    status: DisasterAreaStatus = DisasterAreaStatus.ACTIVE
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    resolved_at: Optional[datetime] = None


class DisasterAreaUpdateDTO(BaseModel):
    id: str  # String ID representing MongoDB ObjectID
    status: DisasterAreaStatus

    @field_validator("id", mode="after")
    @classmethod
    def is_object_id_str(cls, value: str) -> str:
        try:
            _ = ObjectId(value)
        except Exception as e:
            raise ValueError(
                f"{value} is not a string representing valid ObjectID."
            ) from e

        return value
