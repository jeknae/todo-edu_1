from sqlalchemy import select

# user modules
import database.models as models
from database.database import new_session

from schemas.tasks import TaskAdd as STaskAdd


class TaskRepository:
    @classmethod
    async def add(cls, task: STaskAdd):
        """
            Add new task on DataBase:
            params:
            - task: TaskAdd - pydantic model
            
            Return:
            - task: Task - ORM model
        """
        async with new_session() as session:
            task_dict = task.model_dump()

            new_task = models.Task(**task_dict)
            session.add(new_task)
            await session.flush()
            await session.commit()
            return new_task


    @classmethod
    async def get(cls, task_id: int):
        """
            Return one task by task_id
        """
        async with new_session() as session:
            query = select(models.Task).where(models.Task.id == task_id)
            result = await session.execute(query)
            return result.scalars().one()


    @classmethod
    async def get_all(cls):
        """
            Return list of all tasks
        """
        async with new_session() as session:
            query = select(models.Task)
            result = await session.execute(query)
            return result.scalars().all()
