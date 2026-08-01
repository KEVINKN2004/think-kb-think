from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.config import settings
from app.core.embeddings import EmbeddingProvider, get_provider
from app.core.generation import (
    GenerationUnavailable,
    LLMClient,
    generate_answer,
    get_llm,
)
from app.core.retrieval import retrieve
from app.db.schemas import AskRequest, AskResponse, SearchResult
from app.db.session import get_db
from app.limiter import limiter

router = APIRouter(prefix = "/ask", tags = ["ask"])

@router.post("", response_model = AskResponse)
@limiter.limit(settings.rate_limit_ask)
def ask(request: Request, payload: AskRequest, db: Session = Depends(get_db), embedder: EmbeddingProvider = Depends(get_provider), llm: LLMClient = Depends(get_llm),):
    chunks = retrieve(
        db,
        payload.question,
        embedder,
        top_k = payload.top_k,
        min_similarity = settings.min_similarity_threshold,
    )

    try:
        result = generate_answer(payload.question, chunks, llm = llm)
    except GenerationUnavailable:
        raise HTTPException(
            status_code = status.HTTP_503_SERVICE_UNAVAILABLE,
            detail = "The answer service is temporarily unavailable. Please try again later."
    ) from None

    return AskResponse(
        question = payload.question,
        answer = result.answer,
        sources = [SearchResult(**vars(c)) for c in result.sources],
    )