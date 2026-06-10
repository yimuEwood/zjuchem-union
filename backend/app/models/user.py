from sqlalchemy import Column, Integer, String, DateTime, Text, func
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    name = Column(String(50), nullable=False)
    department = Column(String(50), default="")
    role = Column(String(20), default="干事", comment="干事/副部长/部长")
    phone = Column(String(20), default="")
    email = Column(String(100), default="")
    created_at = Column(DateTime, server_default=func.now())
