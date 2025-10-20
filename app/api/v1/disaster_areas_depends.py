from app.models.api.disaster_area import DisasterAreaSearchQueryParam
from app.models.embedded.enums import DisasterAreaStatus


async def disaster_area_search_query_params(
    status: DisasterAreaStatus | None = None,
) -> DisasterAreaSearchQueryParam:
    return DisasterAreaSearchQueryParam(status=status)
