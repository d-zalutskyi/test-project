from fastapi import FastAPI

from app.db.database import create_tables
from app.api.routers import task_router


app = FastAPI(title="Main API")
app.include_router(task_router)


@app.on_event("startup")
async def startup():
    await create_tables()
