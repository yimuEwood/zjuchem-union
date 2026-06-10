from sqlalchemy import Column, Integer, String, DateTime, Text, func
from app.core.database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    department = Column(String(50), default="")
    assignee = Column(String(50), default="")
    deadline = Column(String(20), default="")
    description = Column(Text, default="")
    status = Column(String(20), default="待开始")
    progress = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
