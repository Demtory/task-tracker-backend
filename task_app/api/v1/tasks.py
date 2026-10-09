from fastapi import APIRouter, Depends, HTTPException
from schemas import TaskIn
from services.tasks import TaskService
from schemas.tasks import UpdateTaskRequest

router = APIRouter(tags=["tasks"])


@router.get("/tasks", status_code=200)
def get_tasks(service: TaskService = Depends()):
    return service.get_all_tasks()

@router.get("/tasks/{task_id}", status_code=200)
def get_task_by_id(
    task_id: int,
    service: TaskService = Depends(),
):
    result = service.get_task_by_id(task_id)

    if result["success"]:
        return {
            "id": result["id"],
            "title": result["title"],
            "priority": result["priority"],
        }

    raise HTTPException(
        status_code=404,
        detail=result["message"],
    )

@router.post("/tasks", status_code=201)
def post_tasks(
    task: TaskIn,
    service: TaskService = Depends(),
) -> dict:

    return service.create_task(task)

@router.patch("/tasks/{task_id}", status_code=200)
def update_task(
    task_id: int,
    upd_data: UpdateTaskRequest,
    service: TaskService = Depends(),
):
    result = service.edit_task(task_id, upd_data)

    if result["success"]:
        return {
            "id": result["id"],
            "title": result["title"],
            "priority": result["priority"],
        }

    raise HTTPException(
        status_code=404,
        detail=result["message"],
    )

@router.delete("/tasks/{task_id}", status_code=200)
def delete_task(
    task_id: int,
    service: TaskService = Depends(),
):
    result = service.delete_task(task_id)

    if result["success"]:
        return result

    raise HTTPException(
        status_code=404,
        detail=result["message"],
    )