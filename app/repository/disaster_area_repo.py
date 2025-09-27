from app.models.db.disaster_area import DisasterAreaDocument
from app.models.DTO.disaster_area import DisasterAreaCreateDTO


async def create_disaster_area(
    disaster_area: DisasterAreaCreateDTO,
) -> DisasterAreaCreateDTO:
    disaster_area_doc = DisasterAreaDocument(**disaster_area.model_dump())
    await disaster_area_doc.insert()

    return disaster_area
