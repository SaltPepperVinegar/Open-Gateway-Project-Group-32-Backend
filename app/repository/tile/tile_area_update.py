from datetime import datetime, timezone

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
            area=update.area,
        )
    else:
        area = TilingAreaDoc(
            area_id=update.area_id,
            tiling_version=doc.tiling_version + 1,
            spacing_m=update.spacing_m,
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

    await area.insert()

    return area
