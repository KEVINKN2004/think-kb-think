from app.core.embeddings import get_provider
from app.db.models import Chunk
from app.db.session import SessionLocal


def reembed():
    provider = get_provider()
    db = SessionLocal()
    try:
        chunks = db.query(Chunk).all()
        texts = [c.chunk_text for c in chunks]
        vectors = provider.embed(texts)
        for chunk, vector in zip(chunks, vectors):
            setattr(chunk, provider.column_name, vector)
        db.commit()
        print(f"Re-embedded {len(chunks)} chunks with provider '{provider.name}'.")
    finally:
        db.close()

if __name__ == "__main__":
    reembed()