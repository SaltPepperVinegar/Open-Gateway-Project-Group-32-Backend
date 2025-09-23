from contextlib import asynccontextmanager

from beanie import init_beanie
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
import firebase_admin
from firebase_admin import credentials, get_app

from app.api.v1.users import router as users_router
from app.core.config import settings
from app.models.db.user import UserDocument


@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup ---

    # Mongo / Beanie
    db_client = AsyncIOMotorClient(settings.MONGO_DSN)
    db = db_client.get_default_database()
    await init_beanie(database=db, document_models=[UserDocument])
    app.state.mongo_client = db_client
    app.state.db = db

    # Firebase Admin
    try:
        fb_app = get_app()  # 已有实例则直接复用
    except ValueError:
        cred = credentials.Certificate(settings.FIREBASE_CRED_PATH)
        fb_app = firebase_admin.initialize_app(cred)
    app.state.firebase_app = fb_app

    
    try:
        yield
    finally:
        # --- Shutdown ---
        db_client.close()


app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)

# Routers
app.include_router(users_router)


# Health checks
@app.get("/healthz", include_in_schema=False, tags=["health"])
@app.get("/health", include_in_schema=False, tags=["health"])
async def health():
    return {"status": "ok"}
