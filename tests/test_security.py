DOC = {"title": "Test", "content": "some content about deployment"}


def test_create_rejected_without_api_key(guarded_client):
    response = guarded_client.post("/documents", json = DOC)
    assert response.status_code == 401


def test_create_rejected_with_wrong_api_key(guarded_client):
    response = guarded_client.post("/documents", json = DOC, headers = {"X-API-Key": "wrong"})
    assert response.status_code == 401


def test_create_accepted_with_correct_api_key(guarded_client):
    response = guarded_client.post("/documents", json = DOC, headers = {"X-API-Key": "test-key-123"})
    assert response.status_code == 201


def test_delete_requires_api_key(guarded_client):
    response = guarded_client.delete("/documents/1")
    assert response.status_code == 401


def test_put_requires_api_key(guarded_client):
    response = guarded_client.put("/documents/1", json = DOC)
    assert response.status_code == 401


def test_reads_are_public(guarded_client):
    assert guarded_client.get("/documents").status_code == 200


def test_ask_is_public(guarded_client):
    response = guarded_client.post("/ask", json={"question": "anything"})
    assert response.status_code == 200


def test_oversized_document_rejected(client):
    from app.config import settings

    original = settings.max_chunks_per_document
    settings.max_chunks_per_document = 2
    try:
        response = client.post("/documents", json={"title": "Big", "content": "x" * 5000})
        assert response.status_code == 422
    finally:
        settings.max_chunks_per_document = original


def test_ask_returns_503_when_llm_fails(client):
    from app.core.generation import get_llm
    from app.main import app

    class BrokenLLM:
        def complete(self, prompt: str) -> str:
            raise RuntimeError("upstream provider exploded")

    app.dependency_overrides[get_llm] = lambda: BrokenLLM()
    client.post("/documents", json = DOC)
    response = client.post("/ask", json={"question": "what about deployment?"})
    assert response.status_code == 503
    assert "exploded" not in response.text  