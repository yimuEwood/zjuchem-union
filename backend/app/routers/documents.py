import os
import uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.document import Document

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter(prefix="/documents", tags=["documents"])

def fmt_size(byte_count: int) -> str:
    if byte_count < 1024:
        return f"{byte_count}B"
    elif byte_count < 1024 * 1024:
        return f"{byte_count / 1024:.1f}KB"
    return f"{byte_count / 1024 / 1024:.1f}MB"

@router.get("")
def list_docs(
    department: str = Query(default=None),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    q = db.query(Document)
    if department:
        q = q.filter(Document.department == department)
    return q.order_by(Document.created_at.desc()).all()

@router.post("/upload")
async def upload(
    file: UploadFile = File(...),
    department: str = Query(default="办公室"),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    ext = os.path.splitext(file.filename)[1] if file.filename else ""
    store_name = f"{uuid.uuid4().hex}{ext}"
    store_path = os.path.join(UPLOAD_DIR, store_name)
    content = await file.read()
    with open(store_path, "wb") as f:
        f.write(content)
    doc = Document(
        filename=file.filename or "unknown",
        filepath=store_name,
        size=fmt_size(len(content)),
        department=department,
        uploader=user.get("name", ""),
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc

@router.get("/{doc_id}/download")
def download(doc_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="文件不存在")
    file_path = os.path.join(UPLOAD_DIR, doc.filepath)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="文件已被删除")
    return FileResponse(file_path, filename=doc.filename)

@router.delete("/{doc_id}")
def delete_doc(doc_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="文件不存在")
    file_path = os.path.join(UPLOAD_DIR, doc.filepath)
    if os.path.exists(file_path):
        os.remove(file_path)
    db.delete(doc)
    db.commit()
    return {"detail": "ok"}
