from datetime import datetime, timedelta, timezone
from typing import Optional

from pymongo import ReturnDocument

from app.models.db.tile_area import TilingAreaDoc
from app.models.DTO.tile import TileAreaUpdateDTO


async def update_tile_area(update: TileAreaUpdateDTO) -> TilingAreaDoc:

    doc = await (
        TilingAreaDoc.find({"area_id": update.area_id})
        .sort("-tiling_version")
        .first_or_none()
    )
    if doc is None:
        area = TilingAreaDoc(
            area_id=update.area_id,
            tiling_version=0,
            spacing_m=update.spacing_m,
            update_interval_seconds=update.update_interval_seconds,
            area=update.area,
        )
    else:
        area = TilingAreaDoc(
            area_id=update.area_id,
            tiling_version=doc.tiling_version + 1,
            spacing_m=update.spacing_m,
            update_interval_seconds=update.update_interval_seconds,
            area=update.area,
        )

    await TilingAreaDoc.find(
        {"area_id": update.area_id, "status": {"$eq": "active"}}
    ).update_many(
        {
            "$set": {
                "status": "stale",
                "updated_at": datetime.now(timezone.utc),
            }
        }
    )
    print(f"update tile area {area.area_id}, version: {area.tiling_version}")

    await area.insert()

    return area


async def claim_one_area_need_location_update(
    lock_hold: timedelta = timedelta(minutes=5),
) -> Optional[TilingAreaDoc]:
    """
    Atomically 'claim' a single due area by pushing its next_update_at forward briefly
    (lock_hold) so other schedulers won't pick it up at the same time.
    Returns the claimed area (as a TilingAreaDoc), or None if none available.
    """
    col = TilingAreaDoc.get_pymongo_collection()
    now = datetime.now(timezone.utc)
    claimed_raw = await col.find_one_and_update(
        {
            "status": "active",
            "next_update_at": {"$lte": now},
        },
        {"$set": {"next_update_at": now + lock_hold}},
        return_document=ReturnDocument.BEFORE,
        sort=[("next_update_at", 1)],
    )

    if not claimed_raw:
        return None
    return TilingAreaDoc.model_validate(claimed_raw)
