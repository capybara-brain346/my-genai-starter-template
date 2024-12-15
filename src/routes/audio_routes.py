from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import Optional
from app.models.audio_models import GeminiAudioUtils
from pydantic import BaseModel

router = APIRouter(prefix="/api/audio", tags=["audio"])

audio = GeminiAudioUtils()


class AudioResponse(BaseModel):
    text: str


@router.post("/transcribe", response_model=AudioResponse)
async def transcribe_audio(
    audio_file: UploadFile = File(...), language: str = Form("en-US")
):
    """
    Transcribe audio file to text in the specified language.
    """
    try:
        audio_content = await audio_file.read()
        response = await audio.transcribe_audio(
            audio_input=audio_content, language=language
        )
        return {"text": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze", response_model=AudioResponse)
async def analyze_audio(
    audio_file: UploadFile = File(...),
    prompt: Optional[str] = Form(None),
    language: str = Form("en-US"),
    temperature: float = Form(0.7),
):
    """
    Analyze audio content based on an optional prompt with configurable parameters.
    """
    try:
        audio_content = await audio_file.read()
        response = await audio.analyze_audio_content(
            audio_input=audio_content,
            prompt=prompt,
            language=language,
            temperature=temperature,
        )
        return {"text": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/summarize", response_model=AudioResponse)
async def summarize_audio(
    audio_file: UploadFile = File(...),
    max_length: Optional[int] = Form(None),
    language: str = Form("en-US"),
    temperature: float = Form(0.7),
):
    """
    Generate a concise summary of the audio content with optional length control.
    """
    try:
        audio_content = await audio_file.read()
        response = await audio.summarize_audio(
            audio_input=audio_content,
            max_length=max_length,
            language=language,
            temperature=temperature,
        )
        return {"text": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
