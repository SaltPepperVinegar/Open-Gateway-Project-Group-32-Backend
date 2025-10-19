from typing import Annotated, Any, Dict, List

from fastapi import APIRouter, Depends

from app.api.v1.users_depends import get_decoded_token
from app.models.api.survivor_report import (
    SurvivorReportCreateReq,
    SurvivorReportCreateRes,
    SurvivorReportRetrieveRes,
)
from app.service.survivor_report_service import (
    create_survivor_report_service,
    retrieve_all_survivor_report_service,
)

router = APIRouter(prefix="/survivor_reports", tags=["survivor_reports"])


@router.post("", response_model=SurvivorReportCreateRes, status_code=201)
async def submit_survivor_report(
    req: SurvivorReportCreateReq,
) -> SurvivorReportCreateRes:
    return await create_survivor_report_service(req)


@router.get("", response_model=List[SurvivorReportRetrieveRes], status_code=200)
async def retrieve_all_survivor_reports(
    _: Annotated[Dict[str, Any], Depends(get_decoded_token)],
) -> List[SurvivorReportRetrieveRes]:
    return await retrieve_all_survivor_report_service()
