from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.core.embeddings import EmbeddingProvider
from app.db.models import Chunk, Document


@dataclass
class RetrievedChunk:
    chunk_id: int
    document_id: int
    document_title: str
    chunk_text: str
    similarity: float

def retrieve(db: Session, question: str, provider: EmbeddingProvider, top_k: int = 5, min_similarity: float = 0.0,) -> list[RetrievedChunk]:
    """Find the chunks most semantically similar to the question."""
    if not question.strip():
        return []

    query_vector = provider.embed([question])[0]
    column = getattr(Chunk, provider.column_name)
    distance = column.cosine_distance(query_vector).label("distance")

    rows = (db.query(Chunk, Document.title, distance).join(Document, Chunk.document_id == Document.id).filter(column.isnot(None)).order_by(distance).limit(top_k).all())

    results = []
    for chunk, title, dist in rows:
        similarity = 1.0 - float(dist)
        if similarity >= min_similarity:
            results.append(
                RetrievedChunk(
                    chunk_id=chunk.id,
                    document_id=chunk.document_id,
                    document_title=title,
                    chunk_text=chunk.chunk_text,
                    similarity=similarity,
                )
            )
    return results