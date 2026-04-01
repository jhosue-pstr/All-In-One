import sys
import os
sys.path.insert(0, "/app")
sys.path.insert(0, "/app/packages")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.api import auth_router, sites_router, public_router
from app.db.database import engine
from packages.core.models import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="CMS API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(sites_router)

app.include_router(public_router)


@app.get("/")
def read_root():
    return {"message": "CMS API funcionando", "version": "1.0.0"}
