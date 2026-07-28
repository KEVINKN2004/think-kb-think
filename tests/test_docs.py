def test_create_document(client):
    response = client.post("/documents", json = {"title": "Deploy Guide", "content": "Run docker compose up."})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Deploy Guide"
    assert "id" in data

def test_list_documents(client):
    client.post("/documents", json = {"title": "Doc", "content": "content a"})
    client.post("/documents", json = {"title": "Doc", "content": "content b"})
    response = client.get("/documents")
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_get_document_found(client):
    created = client.post("/documents", json = {"title": "Doc", "content": "stuff"}).json()
    response = client.get(f"/documents/{created['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_get_document_not_found(client):
    response = client.get("/documents/9999")
    assert response.status_code == 404


def test_update_document(client):
    created = client.post("/documents", json = {"title": "Old Title", "content": "old content"}).json()
    response = client.put(
        f"/documents/{created['id']}",
        json = {"title": "New Title", "content": "new content"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New Title"
    assert data["content"] == "new content"
    assert data["id"] == created["id"]  

def test_update_document_not_found(client):
    response = client.put(
        "/documents/9999",
        json = {"title": "Whatever", "content": "does not exist"},
    )
    assert response.status_code == 404

def test_delete_document(client):
    created = client.post("/documents", json = {"title": "Doc", "content": "stuff"}).json()
    delete_response = client.delete(f"/documents/{created['id']}")
    assert delete_response.status_code == 204

    get_response = client.get(f"/documents/{created['id']}")
    assert get_response.status_code == 404


def test_delete_document_not_found(client):
    response = client.delete("/documents/9999")
    assert response.status_code == 404
