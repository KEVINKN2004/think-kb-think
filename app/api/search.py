from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.config import settings
from app.core.embeddings import EmbeddingProvider, get_provider
from app.core.retrieval import retrieve
from app.db.schemas import SearchRequest, SearchResponse, SearchResult
from app.db.session import get_db
from app.limiter import limiter

router = APIRouter(prefix = "/search", tags = ["search"])

@router.post("", response_model = SearchResponse)
@limiter.limit(settings.rate_limit_search)
def search(request: Request, payload: SearchRequest, db: Session = Depends(get_db), embedder: EmbeddingProvider = Depends(get_provider),
):
    results = retrieve(db, payload.question, embedder, top_k = payload.top_k, min_similarity = payload.min_similarity,
    )
    return SearchResponse(question = payload.question, results = [SearchResult(**vars(r)) for r in results],
    )