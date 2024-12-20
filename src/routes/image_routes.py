from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import List, Optional
from src.models.image_models import GeminiVisionUtils
from pydantic import BaseModel

router = APIRouter(prefix="/api/image", tags=["image"])

vision = GeminiVisionUtils()


class ImageAnalysisResponse(BaseModel):
    text: str


@router.post("/analyze", response_model=ImageAnalysisResponse)
async def analyze_image(
    image: UploadFile = File(...),
    prompt: str = Form(...),
    temperature: Optional[float] = Form(0.7),
):
    """
    Analyze a single image with Gemini Vision based on the provided prompt.
    """
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
    """
    Analyze multiple images together with Gemini Vision using a single prompt.
    """
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
    """
    Compare two images and generate a description of their similarities and differences.
    """
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
