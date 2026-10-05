from fastapi import FastAPI, HTTPException
from app.schema import ChatRequest
from app.services.context_service import get_context
from app.llm import get_llm_response

app = FastAPI()

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }

@app.post("/chat")
def chat(request: ChatRequest):
    context = get_context(
        request.client_id,
        request.ticker
    )

    if context is None:
        raise HTTPException(
            status_code=404,
            detail="Client not found"
        )

    answer = get_llm_response(
        context,
        request.user_query
    )

    return {
        "answer": answer
    }