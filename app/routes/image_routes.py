from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import List, Optional
from app.models.image_models import GeminiVisionUtils
from pydantic import BaseModel
import os

router = APIRouter(prefix="/api/image", tags=["image"])

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
vision = GeminiVisionUtils(GOOGLE_API_KEY)


class ImageAnalysisResponse(BaseModel):
    text: str


@router.post("/analyze", response_model=ImageAnalysisResponse)
async def analyze_image(
    image: UploadFile = File(...),
    prompt: str = Form(...),
    temperature: Optional[float] = Form(0.7),
):
    try:
        image_content = await image.read()
        response = await vision.analyze_image(
            image=image_content, prompt=prompt, temperature=temperature
        )
        return {"text": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze-multiple", response_model=ImageAnalysisResponse)
async def analyze_multiple_images(
    images: List[UploadFile] = File(...),
    prompt: str = Form(...),
    temperature: Optional[float] = Form(0.7),
):
    try:
        image_contents = [await img.read() for img in images]
        response = await vision.analyze_multiple_images(
            images=image_contents, prompt=prompt, temperature=temperature
        )
        return {"text": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/compare", response_model=ImageAnalysisResponse)
async def compare_images(
    image1: UploadFile = File(...),
    image2: UploadFile = File(...),
    prompt: Optional[str] = Form(None),
    temperature: Optional[float] = Form(0.7),
):
    try:
        image1_content = await image1.read()
        image2_content = await image2.read()
        response = await vision.compare_images(
            image1=image1_content,
            image2=image2_content,
            prompt=prompt,
            temperature=temperature,
        )
        return {"text": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
