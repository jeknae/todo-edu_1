from fastapi import FastAPI

from contextlib import asynccontextmanager

# user modules
import database.models as models
from routers.tasks import router as task_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await models.drop_tables()
    await models.create_tables()
    print("DB is created")
    yield
    print("App is closing")
    await models.drop_tables()


app = FastAPI(lifespan=lifespan)
app.include_router(task_router)

