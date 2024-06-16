from collections.abc import Sequence
from sqlalchemy import select, delete

# user modules
import database.models as models
from database.database import new_session

from schemas.tasks import TaskAdd as STaskAdd


class TaskRepository:
    @classmethod
    async def add(cls, task: STaskAdd) -> models.Task:
        """
        Add new task.

        Parameters
        ----------
        task: TaskAdd (pydantic model)
            
        Returns
        -------
        task: Task (ORM model)
        
        """
        async with new_session() as session:
            task_dict = task.model_dump()

            new_task = models.Task(**task_dict)
            session.add(new_task)
            await session.flush()
            await session.commit()
            return new_task

    @classmethod
    async def delete(cls, task_id: int) -> dict:
        """
        Remove task  by task id.

        Parameters
        ----------
        task_id: int

        Returns
        -------
        msg: {'deleted': task_id}

        """
        async with new_session() as session:
            query = delete(models.Task).where(models.Task.id == task_id)
            await session.execute(query)
            await session.commit()
            return {'deleted': task_id}
            

    @classmethod
    async def get(cls, task_id: int) -> models.Task:
        """
        Return one task by task id.

        Parameters
        ----------
        task_id: int

        Returns
        -------
        task: models.Task

        """
        async with new_session() as session:
            query = select(models.Task).where(models.Task.id == task_id)
            result = await session.execute(query)
            return result.scalars().one()


    @classmethod
    async def get_all(cls) -> Sequence[models.Task]:
        """
        Return list of all tasks.

        Parameters
        ----------
        None

        Returns
        -------
        tasks: Sequence[models.Task]

        """
        async with new_session() as session:
            query = select(models.Task)
            result = await session.execute(query)
            return result.scalars().all()
