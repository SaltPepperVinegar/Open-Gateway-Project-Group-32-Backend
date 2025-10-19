import asyncio
import json
from contextlib import asynccontextmanager, suppress
from datetime import timezone
from typing import cast

import firebase_admin
from beanie import init_beanie
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from firebase_admin import credentials, get_app
from motor.motor_asyncio import AsyncIOMotorClient

from app.api.v1.disaster_areas import router as disaster_areas_router
from app.api.v1.retrieve_population_data import router as population_router
from app.api.v1.tile_area_update_service_test import router as tiles_router
from app.api.v1.users import router as users_router
from app.api.v1.survivor_reports import router as survivor_reports_router
from app.core.config import settings
from app.models.db.disaster_area import DisasterAreaDocument
from app.models.db.tile import TileDoc
from app.models.db.tile_area import TilingAreaDoc
from app.models.db.tiling_job import TilingJobDoc
from app.models.db.user import UserDocument
from app.models.db.survivor_report import SurvivorReportDocument
from app.service.tile_job_queue_service import tile_queue_loop
from app.service.tile_job_timer_service import tile_area_update_loop

DB_DOCUMENT_MODELS = [
    UserDocument,
    TileDoc,
    TilingJobDoc,
    TilingAreaDoc,
    DisasterAreaDocument,
    SurvivorReportDocument
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup ---

    # Mongo / Beanie
    db_client = AsyncIOMotorClient(
        settings.MONGO_DSN, tz_aware=True, tzinfo=timezone.utc
    )
    db = db_client.get_database(settings.DB_NAME)
    await init_beanie(database=db, document_models=DB_DOCUMENT_MODELS)
    app.state.mongo_client = db_client
    app.state.db = db

    # Firebase Admin
    try:
        fb_app = get_app()  # Reuse Firebase instance if exists
    except ValueError:
        cred_json = cast(str, settings.FIREBASE_CRED)
        cred = credentials.Certificate(json.loads(cred_json))
        fb_app = firebase_admin.initialize_app(cred)
    app.state.firebase_app = fb_app

    jobs_coll = app.state.db.get_collection("tiling_jobs")
    app.state.jobs_coll = jobs_coll

    tile_queue = asyncio.create_task(
        tile_queue_loop(poll_interval_s=2.0, batch_size=200, tile_concurrency=10)
    )

    tile_update = asyncio.create_task(tile_area_update_loop(poll_interval_s=2.0))

    app.state.worker_task = tile_queue

    try:
        yield
    finally:
        tile_queue.cancel()
        with suppress(asyncio.CancelledError):
            await tile_queue
        tile_update.cancel()
        with suppress(asyncio.CancelledError):
            await tile_update

        db_client.close()


app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(users_router, prefix="/api/v1")
app.include_router(tiles_router, prefix="/api/v1")
app.include_router(disaster_areas_router, prefix="/api/v1")
app.include_router(population_router, prefix="/api/v1")
app.include_router(survivor_reports_router, prefix="/api/v1")


# Health checks
@app.get("/healthz", include_in_schema=False, tags=["health"])
@app.get("/health", include_in_schema=False, tags=["health"])
async def health():
    return {"status": "ok"}


for r in app.routes:
    print(getattr(r, "path", None), getattr(r, "methods", None))
