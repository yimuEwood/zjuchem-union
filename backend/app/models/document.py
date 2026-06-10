from sqlalchemy import Column, Integer, String, DateTime, func
from app.core.database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String(255), nullable=False)
    filepath = Column(String(500), nullable=False)
    size = Column(String(20), default="")
    department = Column(String(50), default="")
    uploader = Column(String(50), default="")
    created_at = Column(DateTime, server_default=func.now())
