from typing import List

from app.models.api.survivor_report import (
    SurvivorReportCreateReq,
    SurvivorReportCreateRes,
    SurvivorReportRetrieveRes,
)
from app.models.db.survivor_report import SurvivorReportDocument
from app.models.DTO.survivor_report import SurvivorReportCreateDTO
from app.repository.survivor_report_repo import (
    create_survivor_report,
    get_all_survivor_reports,
)


async def create_survivor_report_service(
    create_req: SurvivorReportCreateReq,
) -> SurvivorReportCreateRes:
    report_create_dto = SurvivorReportCreateDTO(**create_req.model_dump())
    created_report_dto = await create_survivor_report(report_create_dto)

    return SurvivorReportCreateRes(**created_report_dto.model_dump())


async def retrieve_all_survivor_report_service() -> List[SurvivorReportRetrieveRes]:
    reports_dto = await get_all_survivor_reports()
    response_list = [
        SurvivorReportRetrieveRes(**report_dto.model_dump())
        for report_dto in reports_dto
    ]

    return response_list


async def resolve_survivor_report_service(
    id: str,
) -> bool:

    report = await SurvivorReportDocument.get_by_id(str)

    if report:
        await report.delete()
        return True
    else:
        return False
