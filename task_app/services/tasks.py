from fastapi import Depends

from repositories.tasks import TaskRepository
from schemas.tasks import TaskIn, UpdateTaskRequest
from models.tasks import Task


class TaskService:
    def __init__(self, repository: TaskRepository = Depends()):
        self.repository = repository

    def create_task(self, task: TaskIn) -> dict:
        create_result = self.repository.create(task)

        output = task.model_dump()
        output.update({
            "id": create_result.id,
        })

        return output

    def get_all_tasks(self) -> list[Task]:
        return self.repository.get_all()

    def get_task_by_id(self, task_id: int) -> dict:
        task = self.repository.get_by_id(task_id)

        if task is None:
            return {
                "success": False,
                "message": "Задача не найдена.",
            }

        return {
            "success": True,
            "id": task.id,
            "title": task.title,
            "priority": task.priority,
        }

    def edit_task(
        self,
        task_id: int,
        upd_data: UpdateTaskRequest,
    ) -> dict:
        task = self.repository.get_by_id(task_id)

        if task is None:
            return {
                "success": False,
                "message": "Задача не найдена.",
            }

        changes = upd_data.model_dump(
            exclude_unset=True,
            exclude_none=True,
        )

        updated_task = self.repository.edit(task, changes)

        return {
            "success": True,
            "id": updated_task.id,
            "title": updated_task.title,
            "priority": updated_task.priority,
        }

    def delete_task(self, task_id: int) -> dict:
        task = self.repository.get_by_id(task_id)

        if task is None:
            return {
                "success": False,
                "message": "Задача не найдена.",
            }

        self.repository.delete(task)

        return {
            "success": True,
            "message": "Задача удалена.",
        }