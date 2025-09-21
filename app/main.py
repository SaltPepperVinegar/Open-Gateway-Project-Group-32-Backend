from fastapi import FastAPI
from app.core.config import settings

# Mongo/Beanie init
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from app.models.db.user import UserDoc

from app.api.v1.users import router as users_router

app = FastAPI(title=settings.APP_NAME)

@app.on_event("startup")
async def on_startup():
    client = AsyncIOMotorClient(settings.MONGO_DSN)
    db = client.get_default_database()
    await init_beanie(database=db, document_models=[UserDoc])

app.include_router(users_router)

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}


from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    app.state.mongo_client = AsyncIOMotorClient(settings.MONGO_DSN)
    app.state.db = app.state.mongo_client.get_default_database()
    yield
    # shutdown
    app.state.mongo_client.close()

app = FastAPI(lifespan=lifespan)


@app.get("/healthz", include_in_schema=False, tags=["health"])
@app.get("/health", include_in_schema=False, tags=["health"])
async def health():
    return {"status": "ok"}
