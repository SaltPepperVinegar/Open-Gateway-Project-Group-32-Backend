from typing import Any, Dict, List

from app.models.api.population_data import AreaPopulationOut, PopulationWindowIn
from app.models.db.tile_area import TilingAreaDoc


async def retrieve_population_data(req: PopulationWindowIn):
    active_areas = await TilingAreaDoc.find(TilingAreaDoc.status == "active").to_list()
    if not active_areas:
        return []
    active_area_ids = [a.area_id for a in active_areas]
    print("areas:", active_area_ids)

    from app.main import app

    db = app.state.db
    jobs_col = db.get_collection("tiling_jobs")

    time_expr = {}
    if req.time_from:
        time_expr["$gte"] = req.time_from
    if req.time_to:
        time_expr["$lt"] = req.time_to

    match_filter = {
        "status": "completed",
        "area_id": {"$in": active_area_ids},
    }
    if time_expr:
        match_filter["tiling_epoch"] = time_expr

    pipeline = [
        {"$match": match_filter},
        {"$sort": {"area_id": 1, "tiling_version": -1, "tiling_epoch": -1}},
        {
            "$group": {
                "_id": "$area_id",
                "tiling_version": {"$first": "$tiling_version"},
                "tiling_epoch": {"$first": "$tiling_epoch"},
            }
        },
        {
            "$project": {
                "_id": 0,
                "area_id": "$_id",
                "tiling_version": 1,
                "tiling_epoch": 1,
            }
        },
    ]
    latest_jobs = await jobs_col.aggregate(pipeline).to_list()

    if not latest_jobs:
        return []

    print("jobs: ", latest_jobs)
    or_filters = [
        {
            "area_id": job["area_id"],
            "tiling_version": job["tiling_version"],
            "tiling_epoch": job["tiling_epoch"],
        }
        for job in latest_jobs
    ]

    # 4) Geo filter with bbox
    bbox_polygon = bbox_to_polygon(req.bbox)
    geo_filter = {"boundary": {"$geoIntersects": {"$geometry": bbox_polygon}}}

    # 5) Aggregate tiles: match + group by area to compute average density
    tiles_col = db.get_collection("tiles")
    pipeline_tiles = [
        {"$match": {"$and": [geo_filter, {"$or": or_filters}]}},
    ]

    results = await tiles_col.aggregate(pipeline_tiles).to_list(length=None)
    print(len(results))
    return [
        AreaPopulationOut(area=r["boundary"], population=float(r["metrics"]))
        for r in results
    ]


def bbox_to_polygon(bbox: List[float]) -> Dict[str, Any]:
    min_lon, min_lat, max_lon, max_lat = bbox
    if not (min_lon <= max_lon and min_lat <= max_lat):
        raise ValueError("Invalid bbox: ensure min < max for both lon/lat")
    return {
        "type": "Polygon",
        "coordinates": [
            [
                [min_lon, min_lat],
                [max_lon, min_lat],
                [max_lon, max_lat],
                [min_lon, max_lat],
                [min_lon, min_lat],
            ]
        ],
    }
