"""
脚本：初始化/重置数据库 + 创建默认账号 + 示例数据
用法：cd backend && python deploy/init_db.py
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.core.database import engine, Base, SessionLocal
from app.models.user import User
from app.models.task import Task
from app.models.document import Document
from app.core.security import hash_password
from app.core.config import settings

# 确保 data 目录存在
os.makedirs(os.path.dirname(settings.DATABASE_URL.replace("sqlite:///", "")), exist_ok=True)

# 建表
Base.metadata.create_all(bind=engine)
print("✅ 数据库表已创建")

db = SessionLocal()

# 检查是否已有管理员
if not db.query(User).filter(User.username == "admin").first():
    db.add(User(
        username="admin",
        hashed_password=hash_password("admin123"),
        name="管理员",
        department="主席团",
        role="部长",
    ))
    print("✅ 默认管理员已创建 (admin / admin123)")

# 插入示例任务（如果表为空）
if db.query(Task).count() == 0:
    db.add_all([
        Task(title="撰写化学文化节策划案", department="宣传部", assignee="张三", deadline="2026-06-20", status="进行中", progress=60),
        Task(title="整理上学期活动报销单据", department="办公室", assignee="李四", deadline="2026-06-15", status="待开始", progress=0),
        Task(title="联系化工厂参观事宜", department="外联部", assignee="王五", deadline="2026-06-25", status="进行中", progress=30),
        Task(title="化学竞赛报名统计", department="学术部", assignee="赵六", deadline="2026-06-18", status="已完成", progress=100),
    ])
    print("✅ 示例任务已创建")

db.commit()
db.close()
print("🎉 初始化完成！")
