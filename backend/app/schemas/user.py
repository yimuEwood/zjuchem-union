from pydantic import BaseModel as PydanticModel
from typing import Optional

class UserOut(PydanticModel):
    id: int
    username: str
    name: str
    department: str
    role: str
    phone: str
    email: str

    class Config:
        from_attributes = True
