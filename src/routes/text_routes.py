from fastapi import APIRouter, HTTPException
from typing import List, Dict, Optional
from src.models.text_models import GeminiUtils
from pydantic import BaseModel

router = APIRouter(prefix="/api/text", tags=["text"])

gemini = GeminiUtils()


class TextRequest(BaseModel):
    prompt: str
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = None


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Dict[str, str]]
    temperature: Optional[float] = 0.7


class ContextRequest(BaseModel):
    prompt: str
    context: str
    temperature: Optional[float] = 0.7


@router.post("/generate")
async def generate_text(request: TextRequest):
    """
    Generate text using a single prompt.
    """
    try:
        response = await gemini.generate_text(
            prompt=request.prompt,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )
        return {"text": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chat")
async def generate_chat(request: ChatRequest):
    """
    Generate response for a chat conversation.
    """
    try:
        response = await gemini.generate_structured_chat(
            messages=request.messages, temperature=request.temperature
        )
        return {"text": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/context")
async def generate_with_context(request: ContextRequest):
    """
    Generate text with additional context.
    """
    try:
        response = await gemini.generate_with_context(
            prompt=request.prompt,
            context=request.context,
            temperature=request.temperature,
        )
        return {"text": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
