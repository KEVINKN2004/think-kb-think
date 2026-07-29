from datetime import datetime, timezone

from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.session import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key = True, index = True)
    title = Column(String(255), nullable = False)
    content = Column(Text, nullable = False)
    created_at = Column(DateTime, default = lambda: datetime.now(timezone.utc))

    chunks = relationship("Chunk", back_populates = "document", cascade = "all, delete-orphan")

class Chunk(Base):
    __tablename__ = "chunks"

    id = Column(Integer, primary_key = True, index = True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable = False)
    chunk_text = Column(Text, nullable = False)
    embedding_local = Column(Vector(384), nullable = True)
    embedding_api = Column(Vector(1536), nullable = True) 

    document = relationship("Document", back_populates = "chunks")