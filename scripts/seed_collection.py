from pathlib import Path

from app.core.chunking import chunk_text
from app.core.embeddings import get_provider
from app.db.models import Chunk, Document
from app.db.session import SessionLocal

COLLECTION_DIR = Path("evals/collection")


def seed(reset: bool = True):
    provider = get_provider()
    db = SessionLocal()
    try:
        if reset:
            db.query(Chunk).delete()
            db.query(Document).delete()
            db.commit()

        for path in sorted(COLLECTION_DIR.glob("*.md")):
            content = path.read_text(encoding = "utf-8")
            doc = Document(title = path.stem, content = content)
            db.add(doc)
            db.flush()

            pieces = chunk_text(content)
            vectors = provider.embed(pieces)
            for piece, vector in zip(pieces, vectors):
                chunk = Chunk(document_id = doc.id, chunk_text = piece)
                setattr(chunk, provider.column_name, vector)
                db.add(chunk)

            print(f"Seeded '{path.stem}' -> {len(pieces)} chunks")

        db.commit()
        print(f"Committed {db.query(Document).count()} documents.")
    finally:
        db.close()

if __name__ == "__main__":
    seed()