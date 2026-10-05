from app.services.context_service import get_context


def test_get_context():
    context = get_context(1042, "TSLA")

    assert context is not None

def test_get_context_for_existing_client():
    context = get_context(1042, "TSLA")

    assert context is not None

    assert "client_portfolio" in context
    assert "policy" in context
    assert "news" in context

    assert context["client_portfolio"]["client"]["client_id"] == 1042
    assert context["client_portfolio"]["client"]["risk_tolerance"] == "Conservative"

    assert context["policy"] is not None
    assert isinstance(context["news"], list)