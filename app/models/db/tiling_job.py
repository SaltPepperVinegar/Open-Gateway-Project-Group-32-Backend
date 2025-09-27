from datetime import datetime, timezone
from typing import Annotated, Literal, Optional

from beanie import Document, Indexed, PydanticObjectId
from pydantic import Field


class TilingJobDoc(Document):
    area_id: Annotated[PydanticObjectId, Indexed()]

    tiling_version: int
    tiling_epoch: datetime

    status: Literal["queued", "running", "completed", "failed", "canceled"] = "queued"
    priority: int = 0

    total_tiles: int = 0
    processed_tiles: int = 0
    error: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "tiling_jobs"
