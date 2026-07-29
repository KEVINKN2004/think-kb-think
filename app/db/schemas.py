from datetime import datetime

from pydantic import BaseModel, Field


class DocumentCreate(BaseModel):
    title: str = Field(max_length = 225)
    content: str = Field(max_length = 50000)

class DocumentResponse(BaseModel):
    id: int
    title: str = Field(max_length = 225)
    content: str = Field(max_length = 50000)
    created_at: datetime

    model_config = {"from_attributes": True}

class DocumentUpdate(BaseModel):
    title: str = Field(max_length = 255)
    content: str = Field(max_length = 50000)

class SearchRequest(BaseModel):
    question: str = Field(max_length = 1000)
    top_k: int = Field(default = 5, ge = 1, le = 20)
    min_similarity: float = Field(default = 0.0, ge = 0.0, le = 1.0)

class SearchResult(BaseModel):
    chunk_id: int
    document_id: int
    document_title: str
    chunk_text: str
    similarity: float

class SearchResponse(BaseModel):
    question: str
    results: list[SearchResult]

class AskRequest(BaseModel):
    question: str = Field(max_length = 1000)
    top_k: int = Field(default = 5, ge = 1, le = 10)

class AskResponse(BaseModel):
    question: str
    answer: str
    sources: list[SearchResult]