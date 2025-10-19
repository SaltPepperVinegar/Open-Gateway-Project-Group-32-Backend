from typing import List

from app.models.db.survivor_report import SurvivorReportDocument
from app.models.DTO.survivor_report import SurvivorReportCreateDTO, SurvivorReportDTO


async def create_survivor_report(
    new_survivor_report: SurvivorReportCreateDTO,
) -> SurvivorReportDTO:
    survivor_report_doc = SurvivorReportDocument(**new_survivor_report.model_dump())
    await survivor_report_doc.insert()

    survivor_report_doc_dict = survivor_report_doc.model_dump()
    survivor_report_doc_dict["id"] = str(survivor_report_doc.id)

    return SurvivorReportDTO(**survivor_report_doc_dict)


async def get_all_survivor_reports() -> List[SurvivorReportDTO]:
    report_docs = await SurvivorReportDocument.find_all().sort("-created_at").to_list()

    report_dtos = []

    for doc in report_docs:
        doc_dict = doc.model_dump()
        doc_dict["id"] = str(doc.id)
        dto = SurvivorReportDTO(**doc_dict)
        report_dtos.append(dto)

    return report_dtos
