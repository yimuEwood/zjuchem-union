import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine, Base
from app.models.user import User
from app.models.task import Task
from app.models.document import Document
from app.routers import auth, tasks, documents, members

# 自动建表（SQLite 第一次启动时）
Base.metadata.create_all(bind=engine)

app = FastAPI(title="浙大化学系学生会工作站 API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "https://zjuchem.top"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(tasks.router, prefix="/api")
app.include_router(documents.router, prefix="/api")
app.include_router(members.router, prefix="/api")

@app.get("/api/health")
def health():
    return {"status": "ok"}
