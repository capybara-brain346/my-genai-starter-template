
# Google Genai Starter Template

A comprehensive FastAPI starter template for working with Google's Gemini AI models, supporting text, image, and audio processing.

## Features

- **Text Processing**
  - Text generation with prompts
  - Structured chat conversations
  - Context-aware text generation

- **Image Processing**
  - Single image analysis
  - Multiple image analysis
  - Image comparison

- **Audio Processing**
  - Audio transcription
  - Content analysis
  - Audio summarization

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/google-genai-starter-template.git
cd google-genai-starter-template
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install additional audio dependencies:
```bash
# For Ubuntu/Debian
sudo apt-get install ffmpeg

# For macOS
brew install ffmpeg

# For Windows
# Download ffmpeg from https://ffmpeg.org/download.html
```

4. Set up environment variables:
```bash
export GOOGLE_API_KEY="your_api_key_here"
```

## Usage

1. Start the server:
```bash
uvicorn app.main:app --reload
```

2. Access the API documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Text Processing
```bash
POST /api/text/generate
POST /api/text/chat
POST /api/text/context
```

### Image Processing
```bash
POST /api/image/analyze
POST /api/image/analyze-multiple
POST /api/image/compare
```

### Audio Processing
```bash
POST /api/audio/transcribe
POST /api/audio/analyze
POST /api/audio/summarize
```

## Example Requests

### Text Generation
```python
import requests

response = requests.post(
    "http://localhost:8000/api/text/generate",
    json={
        "prompt": "Write a short story about AI",
        "temperature": 0.7
    }
)
print(response.json())
```

### Image Analysis
```python
import requests

files = {
    'image': open('image.jpg', 'rb'),
    'prompt': (None, 'Describe this image'),
    'temperature': (None, '0.7')
}

response = requests.post(
    "http://localhost:8000/api/image/analyze",
    files=files
)
print(response.json())
```

### Audio Processing
```python
import requests

files = {
    'audio_file': open('audio.mp3', 'rb'),
    'language': (None, 'en-US')
}

response = requests.post(
    "http://localhost:8000/api/audio/transcribe",
    files=files
)
print(response.json())
```

## Dependencies

- FastAPI
- google-generativeai
- Pillow
- SpeechRecognition
- pydub
- python-multipart
- uvicorn

## Development

1. Install development dependencies:
```bash
pip install pytest black isort flake8
```

2. Run tests:
```bash
pytest
```

3. Format code:
```bash
black .
isort .
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the GitHub repository.
```
