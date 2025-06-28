from fastapi import APIRouter
from pydantic import BaseModel
from services.gemini_chain import generate_response

router = APIRouter()

class ChatRequest(BaseModel):
    query: str
    history: list[str] = []

@router.post("/chat")
def chat(request: ChatRequest):
    """Chat endpoint for RAG-based product assistance"""
    response, history = generate_response(request.query, request.history)
    return {"response": response, "history": history}