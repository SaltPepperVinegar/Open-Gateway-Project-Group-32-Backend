from contextlib import asynccontextmanager

from beanie import init_beanie
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from app.api.v1.users import router as users_router
from app.core.config import settings
from app.models.db.user import UserDoc


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    client = AsyncIOMotorClient(settings.MONGO_DSN)
    try:
        db = client.get_default_database()
        await init_beanie(database=db, document_models=[UserDoc])
        app.state.mongo_client = client
        app.state.db = db
        yield
    finally:
        # Shutdown
        client.close()


app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)

# Routers
app.include_router(users_router)


# Health checks
@app.get("/healthz", include_in_schema=False, tags=["health"])
@app.get("/health", include_in_schema=False, tags=["health"])
async def health():
    return {"status": "ok"}
