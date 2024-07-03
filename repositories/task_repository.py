from typing import Union

from sqlalchemy import select

from db.database import new_session, TaskOrm
from schemas.task_schemas import STaskAdd, STask


class TaskRepository:
    @classmethod
    async def add_one(cls, data: STaskAdd) -> int:
        async with new_session() as session:
            task_dict = data.model_dump()

            task = TaskOrm(**task_dict)
            session.add(task)
            await session.flush()
            await session.commit()
            return task.id

    @classmethod
    async def find_all(cls) -> list[STask]:
        async with new_session() as session:
            query = select(TaskOrm)
            result = await session.execute(query)
            task_models = result.scalars().all()
            task_schemas = [STask.model_validate(task_model) for task_model in task_models]
            return task_schemas

    @classmethod
    async def find_one(cls, task_id: int) -> Union[STask, list]:
        async with new_session() as session:
            query = select(TaskOrm).where(TaskOrm.id == task_id)
            result = await session.execute(query)
            task = result.scalars().one_or_none()
            if not task:
                return []
            return task