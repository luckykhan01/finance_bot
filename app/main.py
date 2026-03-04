from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.database import db
from app.core.config import settings
from app.api.routes import router as api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"CONNECTING TO: {settings.POSTGRES_USER}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}")

    await db.connect()
    yield
    await db.disconnect()

app = FastAPI(title="Finance Tracker API", lifespan=lifespan)

app.include_router(api_router, prefix='/api', tags=['Transactions'])

@app.get("/")
async def root():
    return {"message": "API is running. DB is connected"}
