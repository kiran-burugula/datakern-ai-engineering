from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_chat_endpoint_with_unknown_client():
    response = client.post(
        "/chat",
        json={
            "client_id": 999999,
            "ticker": "TSLA",
            "user_query": "Can I buy TSLA?"
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Client not found"

def test_chat_endpoint_with_valid_client(monkeypatch):
    fake_context = {
        "client_portfolio": {
            "client": {
                "client_id": 1042,
                "risk_tolerance": "Conservative"
            }
        },
        "policy": {
            "text": "Conservative clients have a 10% limit."
        },
        "news": [
            {
                "title": "Example TSLA news"
            }
        ]
    }

    def fake_get_context(client_id, ticker):
        return fake_context

    def fake_get_llm_response(context, user_query):
        return "This is a test advisory response."

    monkeypatch.setattr(
        "app.main.get_context",
        fake_get_context
    )

    monkeypatch.setattr(
        "app.main.get_llm_response",
        fake_get_llm_response
    )

    response = client.post(
        "/chat",
        json={
            "client_id": 1042,
            "ticker": "TSLA",
            "user_query": "Can I buy TSLA?"
        }
    )

    assert response.status_code == 200
    assert response.json()["answer"] == "This is a test advisory response."

def test_chat_endpoint_with_invalid_client_id():
    response = client.post(
        "/chat",
        json={
            "client_id": "abc",
            "ticker": "TSLA",
            "user_query": "Can I buy TSLA?"
        }
    )

    assert response.status_code == 422