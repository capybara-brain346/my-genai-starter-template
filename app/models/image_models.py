import google.generativeai as genai
from PIL import Image
from typing import Optional, List, Union, BinaryIO
import base64
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()


class GeminiVisionUtils:
    def __init__(self):
        self.model = genai.GenerativeModel("gemini-pro-vision")

    async def _process_image(
        self, image_input: Union[str, bytes, BinaryIO, Image.Image]
    ) -> Image.Image:
        try:

            def process_base64_string(img_input):
                base64_data = img_input.split(",")[1]
                image_data = base64.b64decode(base64_data)
                return Image.open(BytesIO(image_data))

            def process_file_path(img_input):
                return Image.open(img_input)

            input_handlers = {
                str: lambda x: process_base64_string(x)
                if x.startswith("data:image")
                else process_file_path(x),
                bytes: lambda x: Image.open(BytesIO(x)),
                BinaryIO: lambda x: Image.open(x),
                Image.Image: lambda x: x,
            }

            handler = input_handlers.get(type(image_input))
            if handler:
                return handler(image_input)
            raise ValueError("Unsupported image input type")
        except Exception as e:
            raise ValueError(f"Error processing image: {str(e)}")

    async def analyze_image(
        self,
        image: Union[str, bytes, BinaryIO, Image.Image],
        prompt: str,
        temperature: float = 0.7,
    ) -> str:
        """
        Analyze an image and generate text description based on prompt.

        Args:
            image: Image input (file path, bytes, file object, or PIL Image)
            prompt: Text prompt for image analysis
            temperature: Controls randomness (0.0-1.0)

        Returns:
            str: Generated text response
        """
        try:
            processed_image = await self._process_image(image)
            response = await self.model.generate_content_async(
                [prompt, processed_image],
                generation_config={"temperature": temperature},
            )
            return response.text
        except Exception as e:
            print(f"Error analyzing image: {str(e)}")
            return ""

    async def analyze_multiple_images(
        self,
        images: List[Union[str, bytes, BinaryIO, Image.Image]],
        prompt: str,
        temperature: float = 0.7,
    ) -> str:
        """
        Analyze multiple images and generate a combined response.

        Args:
            images: List of image inputs
            prompt: Text prompt for image analysis
            temperature: Controls randomness (0.0-1.0)

        Returns:
            str: Generated text response
        """
        try:
            processed_images = [await self._process_image(img) for img in images]
            response = await self.model.generate_content_async(
                [prompt, *processed_images],
                generation_config={"temperature": temperature},
            )
            return response.text
        except Exception as e:
            print(f"Error analyzing multiple images: {str(e)}")
            return ""

    async def compare_images(
        self,
        image1: Union[str, bytes, BinaryIO, Image.Image],
        image2: Union[str, bytes, BinaryIO, Image.Image],
        prompt: Optional[str] = None,
        temperature: float = 0.7,
    ) -> str:
        """
        Compare two images and generate analysis.

        Args:
            image1: First image input
            image2: Second image input
            prompt: Custom comparison prompt (optional)
            temperature: Controls randomness (0.0-1.0)

        Returns:
            str: Generated comparison text
        """
        try:
            processed_image1 = await self._process_image(image1)
            processed_image2 = await self._process_image(image2)

            default_prompt = "Compare these two images and describe the differences and similarities."
            comparison_prompt = prompt or default_prompt

            response = await self.model.generate_content_async(
                [comparison_prompt, processed_image1, processed_image2],
                generation_config={"temperature": temperature},
            )
            return response.text
        except Exception as e:
            print(f"Error comparing images: {str(e)}")
            return ""


# Example usage:
"""
api_key = "your-api-key"
vision = GeminiVisionUtils(api_key)

# Analyze single image
response = await vision.analyze_image(
    "path/to/image.jpg",
    "Describe what you see in this image"
)

# Analyze multiple images
images = ["image1.jpg", "image2.jpg", "image3.jpg"]
response = await vision.analyze_multiple_images(
    images,
    "Compare these images and describe what they have in common"
)

# Compare two images
comparison = await vision.compare_images(
    "image1.jpg",
    "image2.jpg",
    "What are the main differences between these images?"
)
"""
