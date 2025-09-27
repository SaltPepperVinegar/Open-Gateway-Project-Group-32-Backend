import pytest
from bson import ObjectId

from app.models.db.tile_area import TilingAreaDoc
from app.models.DTO.tile import TileAreaUpdateDTO  # adjust to your path
from app.models.general.geo_json import GeoJSONPolygon
from app.service.tile_update_service import update_tile_area

pytestmark = pytest.mark.asyncio

VALID_POLY = GeoJSONPolygon(
    coordinates=[
        [
            [144.95, -37.82],
            [144.98, -37.82],
            [144.96, -37.78],
            [144.95, -37.80],
            [144.94, -37.79],
            [144.92, -37.79],
            [144.95, -37.82],
        ]
    ]
)


async def test_creates_version_zero_when_no_prior_doc(init_db):

    area_id = ObjectId()
    dto = TileAreaUpdateDTO(
        area=VALID_POLY,
        area_id=area_id,
        spacing_m=200,
    )

    await update_tile_area(dto)

    # Verify: one doc for this area_id, version 0
    docs = await TilingAreaDoc.find(TilingAreaDoc.area_id == area_id).to_list()
    assert len(docs) == 1
    created = docs[0]
    assert created.area_id == area_id
    assert created.spacing_m == 200
    assert created.tiling_version == 0
    assert created.area.model_dump() == dto.area.model_dump()


async def test_increments_version_when_prior_exists(init_db):
    area_id = ObjectId()

    # Seed: two historical versions
    await TilingAreaDoc(
        area_id=area_id, tiling_version=1, spacing_m=150, area=VALID_POLY
    ).insert()
    await TilingAreaDoc(
        area_id=area_id, tiling_version=3, spacing_m=180, area=VALID_POLY
    ).insert()

    dto = TileAreaUpdateDTO(
        area=VALID_POLY,
        area_id=area_id,
        spacing_m=250,
    )
    await update_tile_area(dto)

    # Verify: new latest version == 4 (3 + 1)
    docs = (
        await TilingAreaDoc.find(TilingAreaDoc.area_id == area_id)
        .sort(-TilingAreaDoc.tiling_version)
        .to_list()
    )
    assert len(docs) == 3
    latest = docs[0]
    assert latest.tiling_version == 4
    assert latest.spacing_m == 250
    assert latest.area.model_dump() == dto.area.model_dump()
