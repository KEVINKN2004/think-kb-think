from app.core.embeddings import get_provider
from app.core.retrieval import retrieve
from app.db.models import Chunk
from app.db.session import SessionLocal

db = SessionLocal()
q = "How long do I have to file an 83(b) election?"

target_ids = {c.id for c in db.query(Chunk).filter(Chunk.chunk_text.contains("83(b)")).all()}
print(f"Chunks literally containing '83(b)': {sorted(target_ids)}\n")

results = retrieve(db, q, get_provider(), top_k=20, min_similarity=0.0)
for rank, r in enumerate(results, 1):
    marker = "  <-- CONTAINS ANSWER" if r.chunk_id in target_ids else ""
    print(f"{rank:>3}. {round(r.similarity, 3)}  chunk {r.chunk_id}  {r.document_title}{marker}")