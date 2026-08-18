from app import app


def test_hello():
    client = app.test_client()

    response = client.get("/api/hello")

    assert response.status_code == 200