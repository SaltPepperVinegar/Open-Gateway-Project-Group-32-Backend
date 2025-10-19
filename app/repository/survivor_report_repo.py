from typing import List

from models.DTO.survivor_report import SurvivorReportDTO, SurvivorReportCreateDTO
from models.db.survivor_report import SurvivorReportDocument


async def create_survivor_report(
    new_survivor_report: SurvivorReportCreateDTO
) -> SurvivorReportDTO:
    survivor_report_doc = SurvivorReportDocument(**new_survivor_report.model_dump())
    await survivor_report_doc.insert()

    return SurvivorReportDTO(**survivor_report_doc.model_dump())


async def get_all_survivor_reports() -> List[SurvivorReportDTO]:
    report_docs = await SurvivorReportDocument.find_all().to_list()
    report_dtos = [SurvivorReportDTO(**doc.model_dump()) for doc in report_docs]

    return report_dtos
