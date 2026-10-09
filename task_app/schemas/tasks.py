from pydantic import BaseModel, Field

class TaskIn(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    priority: int = Field(default=1, ge=1, le=5)


class UpdateTaskRequest(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    priority: int | None = Field(default=None, ge=1, le=5)