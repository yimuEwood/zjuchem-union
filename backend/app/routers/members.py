from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.schemas.user import UserOut

router = APIRouter(prefix="/members", tags=["members"])

@router.get("", response_model=list[UserOut])
def list_members(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(User).order_by(User.department, User.role).all()
