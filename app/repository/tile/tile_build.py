# app/services/tiling_service.py
import hashlib
from typing import List

from app.models.db.tile import TileDoc
from app.models.db.tile_area import TilingAreaDoc
from app.models.db.tiling_job import TilingJobDoc
from app.models.general.geo_json import GeoJSONPoint, GeoJSONPolygon
from app.repository.tile.tiling_strategy import tile_strategy_square_centre


def hash_tile(area_id: str, tiling_version: int, boundary: List[List[float]]) -> str:
    # stable hash: area_id + version + rounded coordinates
    s = f"{area_id}:{tiling_version}:" + ";".join(
        f"{x:.7f},{y:.7f}" for x, y in boundary
    )
    return hashlib.sha1(s.encode("utf-8")).hexdigest()


async def build_tiles_and_store(area: TilingAreaDoc, job: TilingJobDoc) -> int:
    rings = area.area.coordinates
    tiles = tile_strategy_square_centre(rings, spacing_m=area.spacing_m)

    bulk: List[TileDoc] = []

    for b in tiles:
        cx = sum(p[0] for p in b[:4]) / 4.0
        cy = sum(p[1] for p in b[:4]) / 4.0
        tkey = hash_tile(str(area.area_id), area.tiling_version, b)
        doc = TileDoc(
            area_id=area.area_id,
            tiling_version=area.tiling_version,
            tiling_epoch=job.tiling_epoch,
            tile_key=tkey,
            boundary=GeoJSONPolygon(coordinates=[b]),
            center=GeoJSONPoint(coordinates=[round(cx, 7), round(cy, 7)]),
        )
        bulk.append(doc)

    if bulk:
        await TileDoc.insert_many(bulk)

    return len(bulk)
