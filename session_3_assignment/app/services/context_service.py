from app.clients.postgres_client import get_client_portfolio

from app.clients.web_search_client import get_stock_news

from PyPDF2 import PdfReader
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

POLICY_FILE = BASE_DIR / "Apex_Financial_Risk_Policy_2026.pdf"

# reader = PdfReader("Apex_Financial_Risk_Policy_2026.pdf")
reader = PdfReader(POLICY_FILE)

def get_policy_rules(risk_tolerance):
    for page_number, page in enumerate(reader.pages):
        text = page.extract_text() or ""

        match_position = text.lower().find(risk_tolerance.lower())

        if match_position != -1:
            start = max(0, match_position - 300)
            end = match_position + 800

            relevant_text = text[start:end]

            return {
                "page": page_number + 1,
                "text": relevant_text
            }

    return None

def get_context(client_id, ticker):
    # 1. call get_client_portfolio
    client_portfolio = get_client_portfolio(client_id)

    # 2. handle None
    if client_portfolio is None:
        return None

    # 3. obtain risk_tolerance
    risk_tolerance = client_portfolio["client"]["risk_tolerance"]

    # 4. call get_policy_rules
    policy = get_policy_rules(risk_tolerance)

    # 5. call get_stock_news
    news = get_stock_news(ticker)

    # 6. combine client_portfolio + policy
    context = {
        "client_portfolio": client_portfolio,
        "policy": policy,
        "news": news
    }

    # 7. return combined context
    return context

if __name__ == "__main__":
    print(get_context(1042, "TSLA"))