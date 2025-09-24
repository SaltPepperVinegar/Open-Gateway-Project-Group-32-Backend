import json
from contextlib import asynccontextmanager
from typing import cast

import firebase_admin
from beanie import init_beanie
from fastapi import FastAPI
from firebase_admin import credentials, get_app
from motor.motor_asyncio import AsyncIOMotorClient

from app.api.v1.users import router as users_router
from app.core.config import settings
from app.models.db.user import UserDocument

DB_DOCUMENT_MODELS = [UserDocument]


@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup ---

    # Mongo / Beanie
    db_client = AsyncIOMotorClient(settings.MONGO_DSN)
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

    try:
        yield
    finally:
        # --- Shutdown ---
        db_client.close()


app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)

# Routers
app.include_router(users_router, prefix="/api/v1")


# Health checks
@app.get("/healthz", include_in_schema=False, tags=["health"])
@app.get("/health", include_in_schema=False, tags=["health"])
async def health():
    return {"status": "ok"}
