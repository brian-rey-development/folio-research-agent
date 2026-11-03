from fastapi.testclient import TestClient
from folio_api.main import create_app

HTTP_OK = 200


def test_health_returns_ok() -> None:
    response = TestClient(create_app()).get("/health")

    assert response.status_code == HTTP_OK
    assert response.json() == {"status": "ok"}
