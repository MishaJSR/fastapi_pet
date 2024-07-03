from typing import Annotated, Union

from fastapi import APIRouter, Depends

from repositories.task_repository import TaskRepository
from schemas.task_schemas import STaskAdd, STask, STaskId

router = APIRouter(
    prefix="/tasks",
    tags=["Работа с задачами"],
)


@router.post("")
async def add_task(task: Annotated[STaskAdd, Depends()],) -> STaskId:
    task_id = await TaskRepository.add_one(task)
    return {"ok": True, "task_id": task_id}


@router.get("")
async def get_tasks() -> list[STask]:
    tasks = await TaskRepository.find_all()
    return tasks

@router.get("/{task_id}")
async def get_tasks_by_id(task_id: int) -> Union[STask, list]:
    task = await TaskRepository.find_one(task_id)
    return task