from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.chunking import chunk_text
from app.core.embeddings import EmbeddingProvider, get_provider
from app.db.models import Chunk, Document
from app.db.schemas import DocumentCreate, DocumentResponse, DocumentUpdate
from app.db.session import get_db
from app.api.auth import require_api_key
from app.config import settings

router = APIRouter(prefix = "/documents", tags = ["documents"])

@router.post("", response_model = DocumentResponse, status_code = status.HTTP_201_CREATED, dependencies = [Depends(require_api_key)])
def create_document(payload: DocumentCreate, db: Session = Depends(get_db), embedder: EmbeddingProvider = Depends(get_provider)):
    doc = Document(title = payload.title, content = payload.content)
    db.add(doc)
    db.flush()

    pieces = chunk_text(payload.content)
    if len(pieces) > settings.max_chunks_per_document:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail = f"Document produces {len(pieces)} chunks, exceeding the limit of {settings.max_chunks_per_document}.",
        )
    vectors = embedder.embed(pieces)
    vectors = embedder.embed(pieces)

    for piece, vector in zip(pieces, vectors):
        chunk = Chunk(document_id = doc.id, chunk_text = piece)
        setattr(chunk, embedder.column_name, vector)
        db.add(chunk)

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

@router.put("/{doc_id}", response_model = DocumentResponse, dependencies = [Depends(require_api_key)])
def update_document(doc_id: int, payload: DocumentUpdate, db: Session = Depends(get_db), embedder: EmbeddingProvider = Depends(get_provider)):
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if doc is None:
        raise HTTPException(status_code=404, detail = "Document not found")
    doc.title = payload.title
    doc.content = payload.content

    db.query(Chunk).filter(Chunk.document_id == doc.id).delete()

    pieces = chunk_text(payload.content)
    if len(pieces) > settings.max_chunks_per_document:
        raise HTTPException(
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail = f"Document produces {len(pieces)} chunks, exceeding the limit of {settings.max_chunks_per_document}.",
        )
    vectors = embedder.embed(pieces)

    for piece, vector in zip(pieces, vectors):
        chunk = Chunk(document_id = doc.id, chunk_text = piece)
        setattr(chunk, embedder.column_name, vector)
        db.add(chunk)

    db.commit()
    db.refresh(doc)
    return doc

@router.delete("/{doc_id}", status_code = status.HTTP_204_NO_CONTENT, dependencies = [Depends(require_api_key)])
def delete_document(doc_id: int, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if doc is None:
        raise HTTPException(status_code = 404, detail = "Document not found")
    db.delete(doc)
    db.commit()