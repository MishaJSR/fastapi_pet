from fastapi import FastAPI
import uvicorn

from contextlib import asynccontextmanager

from db.database import create_tables, delete_tables
from routers.task_router import router as tasks_router
from routers.authorization_router import router as authorization_router

au = {"prefix": "/api/v1"}


@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    print("База очищена")
    await create_tables()
    print("База готова к работе")
    yield
    print("Выключение")


app = FastAPI(lifespan=lifespan)
app.include_router(tasks_router)
app.include_router(authorization_router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8002)