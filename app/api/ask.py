from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config import settings
from app.core.embeddings import EmbeddingProvider, get_provider
from app.core.generation import LLMClient, generate_answer, get_llm
from app.core.retrieval import retrieve
from app.db.schemas import AskRequest, AskResponse, SearchResult
from app.db.session import get_db

router = APIRouter(prefix = "/ask", tags = ["ask"])

@router.post("", response_model = AskResponse)
def ask(payload: AskRequest, db: Session = Depends(get_db), embedder: EmbeddingProvider = Depends(get_provider), llm: LLMClient = Depends(get_llm),):
    chunks = retrieve(
        db,
        payload.question,
        embedder,
        top_k=payload.top_k,
        min_similarity=settings.min_similarity_threshold,
    )
    result = generate_answer(payload.question, chunks, llm = llm)
    return AskResponse(
        question=payload.question,
        answer=result.answer,
        sources=[SearchResult(**vars(c)) for c in result.sources],
    )

from app.core.generation import LLMClient, get_llm
