from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.deps import get_current_user
from app.core.security import verify_password, create_access_token
from app.models.user import User
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["auth"])

class LoginBody(BaseModel):
    username: str
    password: str

@router.post("/login")
def login(body: LoginBody, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == body.username).first()
    if not user or not verify_password(body.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    token = create_access_token(user.id)
    return {
        "token": token,
        "user": {
            "id": user.id,
            "username": user.username,
            "name": user.name,
            "department": user.department,
            "role": user.role,
        },
    }

@router.get("/me")
def get_me(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    u = db.query(User).filter(User.id == current_user["id"]).first()
    if not u:
        raise HTTPException(status_code=404, detail="用户不存在")
    return {"id": u.id, "username": u.username, "name": u.name, "department": u.department, "role": u.role}
