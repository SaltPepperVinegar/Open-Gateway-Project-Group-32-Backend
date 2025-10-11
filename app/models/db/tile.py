from datetime import datetime, timezone
from typing import Annotated, Literal

from beanie import Document, Indexed, PydanticObjectId
from pydantic import Field
from pymongo import ASCENDING, DESCENDING, GEOSPHERE, IndexModel

from app.models.general.geo_json import GeoJSONPoint, GeoJSONPolygon


class TileDoc(Document):
    # ownership
    area_id: Annotated[PydanticObjectId, Indexed()]

    tiling_version: int
    tiling_epoch: datetime

    tile_key: Annotated[str, Indexed()] = Field(
        ..., description="Unique key", unique=True
    )

    boundary: GeoJSONPolygon
    center: GeoJSONPoint

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    metrics: int | None = None
    metrics_updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    status: Literal["pending", "processing", "ready", "failed", "stale"] = "pending"

    class Settings:
        name = "tiles"
        indexes = [
            IndexModel([("tile_key", ASCENDING)]),
            # speed area filtering and latest-sort (pairs with your queries)
            IndexModel(
                [
                    ("area_id", ASCENDING),
                    ("tiling_version", DESCENDING),
                    ("tiling_epoch", DESCENDING),
                ],
            ),
            # geo indexes
            IndexModel([("boundary", GEOSPHERE)]),
            IndexModel([("center", GEOSPHERE)]),
        ]
