from pydantic import BaseModel

class ChatRequest(BaseModel):
    client_id: int
    ticker: str
    user_query: str

# request = ChatRequest(
#     client_id=1042,
#     ticker="TSLA",
#     user_query="Can I buy TSLA?"
# )

# print(request)
# print(request.client_id)
# print(request.ticker)
# print(request.user_query)