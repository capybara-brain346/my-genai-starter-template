from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes import text_routes, image_routes, audio_routes

app = FastAPI(
    title="Gemini AI API",
    description="API for text, image, and audio processing using Google's Gemini models",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(text_routes.router)
app.include_router(image_routes.router)
app.include_router(audio_routes.router)


@app.get("/")
async def root():
    return {
        "message": "Welcome to Gemini AI API",
        "docs": "/docs",
        "endpoints": {
            "text": "/api/text/",
            "image": "/api/image/",
            "audio": "/api/audio/",
        },
    }
