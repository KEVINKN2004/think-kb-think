import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.core.embeddings import MockEmbeddingProvider, get_provider
from app.core.generation import get_llm
from app.db.session import Base, get_db
from app.main import app

TEST_DATABASE_URL = settings.database_url.replace("/kbdb", "/kbdb_test")

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

class StubLLM:
    def complete(self, prompt: str) -> str:
        return "Stubbed answer citing [1]."

@pytest.fixture()
def db_session():
    Base.metadata.create_all(bind = engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind = engine)

@pytest.fixture()
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_provider] = lambda: MockEmbeddingProvider()
    app.dependency_overrides[get_llm] = lambda: StubLLM()
    yield TestClient(app)
    app.dependency_overrides.clear()