from fastapi import FastAPI

# user modules
from routers.tasks import router as task_router
from lifespan import lifespan


app = FastAPI(lifespan=lifespan)
app.include_router(task_router)

