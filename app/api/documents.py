from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.models import Document
from app.db.schemas import DocumentCreate, DocumentResponse, DocumentUpdate
from app.db.session import get_db

router = APIRouter(prefix = "/documents", tags = ["documents"])

@router.post("", response_model = DocumentResponse, status_code = status.HTTP_201_CREATED)
def create_document(payload: DocumentCreate, db: Session = Depends(get_db)):
    doc = Document(title = payload.title, content = payload.content)
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc

@router.get("", response_model = list[DocumentResponse])
def list_documents(db: Session = Depends(get_db)):
    return db.query(Document).all()

@router.get("/{doc_id}", response_model = DocumentResponse)
def get_document(doc_id: int, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if doc is None:
        raise HTTPException(status_code = 404, detail = "Document not found")
    return doc

@router.put("/{doc_id}", response_model = DocumentResponse)
def update_document(doc_id: int, payload: DocumentUpdate, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if doc is None:
        raise HTTPException(status_code=404, detail = "Document not found")
    doc.title = payload.title
    doc.content = payload.content
    db.commit()
    db.refresh(doc)
    return doc

@router.delete("/{doc_id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_document(doc_id: int, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if doc is None:
        raise HTTPException(status_code = 404, detail = "Document not found")
    db.delete(doc)
    db.commit()
