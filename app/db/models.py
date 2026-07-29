from datetime import datetime, timezone

from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer, String, Text
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

Index( "ix_chunks_embedding_local_hnsw", Chunk.embedding_local,
    postgresql_using="hnsw",
    postgresql_with={"m": 16, "ef_construction": 64},
    postgresql_ops={"embedding_local": "vector_cosine_ops"},
)
Index("ix_chunks_embedding_api_hnsw", Chunk.embedding_api,
    postgresql_using="hnsw",
    postgresql_with={"m": 16, "ef_construction": 64},
    postgresql_ops={"embedding_api": "vector_cosine_ops"},
)