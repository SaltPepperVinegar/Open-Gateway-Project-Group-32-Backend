from typing import Optional, List
from datetime import datetime, timezone

from app.models.db.disaster_area import DisasterAreaDocument
from app.models.DTO.disaster_area import DisasterAreaCreateDTO, DisasterAreaDTO, DisasterAreaUpdateDTO
from app.models.embedded.enums import DisasterAreaStatus
from app.exceptions.disaster_area import DisasterAreaDoesNotExistError
from pymongo import DESCENDING
from bson import ObjectId


async def create_disaster_area(
    disaster_area: DisasterAreaCreateDTO,
) -> DisasterAreaCreateDTO:
    disaster_area_doc = DisasterAreaDocument(**disaster_area.model_dump())
    await disaster_area_doc.insert()

    return disaster_area


async def search_disaster_area(
    status: Optional[DisasterAreaStatus]
) -> List[DisasterAreaDTO]:
    if status:
        # Results are sorted with latest updated area at the beginning.
        disaster_area_documents = await DisasterAreaDocument \
            .find(DisasterAreaDocument.status == status) \
            .sort([DisasterAreaDocument.updated_at, DESCENDING]) \
            .to_list()
    else:
        disaster_area_documents = []

        # Prior portion of area data has active status
        disaster_area_documents += await DisasterAreaDocument \
            .find(DisasterAreaDocument.status == DisasterAreaStatus.ACTIVE) \
            .sort([DisasterAreaDocument.updated_at, DESCENDING]) \
            .to_list()
        
        # Latter portion of data has resolved status
        disaster_area_documents += await DisasterAreaDocument \
            .find(DisasterAreaDocument.status == DisasterAreaStatus.RESOLVED) \
            .sort([DisasterAreaDocument.updated_at, DESCENDING]) \
            .to_list()
    
    # Convert search results from document model into general DTO model and return

    disaster_area_dtos = []

    for document in disaster_area_documents:
        document_dict = document.model_dump()
        document_dict["id"] = str(document.id)
        disaster_area_dtos.append(DisasterAreaDTO(**document_dict))

    return disaster_area_dtos


async def update_disaster_area(
    update_info: DisasterAreaUpdateDTO
) -> DisasterAreaDTO:
    target_document = await DisasterAreaDocument.find_one({"_id": ObjectId(update_info.id)})

    if target_document is None:
        raise DisasterAreaDoesNotExistError()

    if update_info.status == DisasterAreaStatus.RESOLVED:
        target_document.status = DisasterAreaStatus.RESOLVED
        target_document.resolved_at = datetime.now(timezone.utc)
    else:
        target_document.status = update_info.status
        target_document.resolved_at = None
    
    await target_document.save()

    target_document_dict = target_document.model_dump()
    target_document_dict["id"] = str(target_document.id)

    return DisasterAreaDTO(**target_document_dict)

