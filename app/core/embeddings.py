from typing import Protocol

from app.config import settings


class EmbeddingProvider(Protocol):
    name: str
    dimensions: int
    column_name: str

    def embed(self, texts: list[str]) -> list[list[float]]: ...

class LocalEmbeddingProvider:
    """MiniLM running locally with no API key."""

    name = "local"
    dimensions = 384
    column_name = "embedding_local"

    def __init__(self) -> None:
        self.model = None

    @property
    def model(self):
        if self.model is None:
            from sentence_transformers import SentenceTransformer

            self.model = SentenceTransformer("all-MinLM-L6-v2")
        return self.model

    def embed(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        return [vector.tolist() for vector in self.model.encode(texts)]

provider_cache: dict[str, EmbeddingProvider] = {}

def get_provider() -> EmbeddingProvider:
    name = settings.embedding_provider
    if name not in provider_cache:
        if name == "local":
            provider_cache[name] = LocalEmbeddingProvider()
        elif name == "openai":
            provider_cache[name] = OpenAIEmbeddingProvider()
        else:
            raise ValueError(f"Unknown embedding provider: {name}")
    return provider_cache[name]

class MockEmbeddingProvider:
    """Deterministic mock vectors, they will be used in tests so that CI never loads in a real model."""

    name = "mock"
    dimensions = 384
    column_name = "embedding_local"

    def embed(self, texts: list[str]) -> list[list[str]]:
        vectors = []
        for text in texts:
            seed = (sum(ord(c) for c in text) % 97) / 97.0
            vectors.append([seed] * self.dimensions)
        return vectors

class OpenAIEmbeddingProvider:
    """Text-embedding-3-small via OpenAI's API."""

    name = "openai"
    dimensions = 1536
    column_name = "embedding_api"

    def __init__(self) -> None:
        from openai import OpenAI

        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY is not set.")
        self.client = OpenAI(api_key = settings.openai_api_key)

    def embed(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        response = self.client.embeddings.create(model = "text-embedding-3-small", inputs = texts,)
        return [item.embedding for item in response.data]