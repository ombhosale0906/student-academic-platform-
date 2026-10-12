def test_health_endpoint(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "UP"


def test_list_books_endpoint(client):
    response = client.get("/api/books")
    assert response.status_code == 200
    assert response.get_json()["count"] == 2


def test_get_user_endpoint(client):
    response = client.get("/api/users/U101")
    assert response.status_code == 200
    assert response.get_json()["name"] == "Alice Johnson"


def test_unknown_user_endpoint(client):
    response = client.get("/api/users/U999")
    assert response.status_code == 404
