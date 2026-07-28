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