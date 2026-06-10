from pydantic import BaseModel as PydanticModel
from typing import Optional

class TaskCreate(PydanticModel):
    title: str
    department: str = ""
    assignee: str = ""
    deadline: str = ""
    description: str = ""

class TaskUpdate(PydanticModel):
    title: Optional[str] = None
    department: Optional[str] = None
    assignee: Optional[str] = None
    deadline: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    progress: Optional[int] = None

class TaskOut(PydanticModel):
    id: int
    title: str
    department: str
    assignee: str
    deadline: str
    description: str
    status: str
    progress: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True

class StatusUpdate(PydanticModel):
    status: str
