from app.core.embeddings import MockEmbeddingProvider
from app.core.retrieval import retrieve


def _add_doc(client, title, content):
    return client.post("/documents", json = {"title": title, "content": content}).json()


def test_retrieve_returns_most_similar_chunk_first(client, db_session):
    _add_doc(client, "Deploy", "To deploy to staging run the docker compose command")
    _add_doc(client, "Cooking", "Bake the sourdough bread at high oven temperature")

    results = retrieve(db_session, "how do I deploy to staging", MockEmbeddingProvider(), top_k = 2)

    assert len(results) > 0
    assert "deploy" in results[0].chunk_text.lower()


def test_retrieve_respects_top_k(client, db_session):
    for i in range(5):
        _add_doc(client, f"Doc {i}", f"unique content number {i} about topic {i}")

    results = retrieve(db_session, "topic", MockEmbeddingProvider(), top_k=2)
    assert len(results) <= 2


def test_retrieve_returns_similarity_scores(client, db_session):
    _add_doc(client, "Deploy", "deploy to staging with docker")

    results = retrieve(db_session, "deploy staging docker", MockEmbeddingProvider(), top_k = 1)

    assert 0.0 <= results[0].similarity <= 1.0


def test_results_ordered_by_similarity_descending(client, db_session):
    _add_doc(client, "A", "deploy staging docker compose command")
    _add_doc(client, "B", "completely unrelated gardening topic here")

    results = retrieve(db_session, "deploy staging docker", MockEmbeddingProvider(), top_k=2)

    scores = [r.similarity for r in results]
    assert scores == sorted(scores, reverse=True)


def test_retrieve_on_empty_database_returns_empty(db_session):
    results = retrieve(db_session, "anything", MockEmbeddingProvider(), top_k=5)
    assert results == []


def test_min_similarity_filters_weak_matches(client, db_session):
    _add_doc(client, "Deploy", "deploy staging docker compose")

    results = retrieve(
        db_session, "quantum astrophysics nebula", MockEmbeddingProvider(),
        top_k = 5, min_similarity = 0.9,
    )
    assert results == []

def test_search_endpoint_returns_results(client):
    client.post("/documents", json={"title": "Deploy", "content": "deploy to staging using docker compose"})

    response = client.post("/search", json = {"question": "how to deploy staging", "top_k": 3})

    assert response.status_code == 200
    body = response.json()
    assert body["question"] == "how to deploy staging"
    assert len(body["results"]) >= 1
    assert "similarity" in body["results"][0]


def test_search_rejects_invalid_top_k(client):
    response = client.post("/search", json={"question": "test", "top_k": 9999})
    assert response.status_code == 422