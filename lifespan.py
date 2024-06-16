import sqlalchemy
from fastapi import FastAPI

from contextlib import asynccontextmanager

# user modules
from database.database import engine, Model


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)


async def drop_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    print("DB is created")
    yield
    print("App is closing")


