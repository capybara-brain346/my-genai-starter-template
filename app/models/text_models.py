import google.generativeai as genai
from typing import Optional, List, Dict
from dotenv import load_dotenv
import os

load_dotenv()


class GeminiUtils:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-pro")

    async def generate_text(
        self, prompt: str, temperature: float = 0.7, max_tokens: Optional[int] = None
    ) -> str:
        try:
            response = await self.model.generate_content_async(
                prompt,
                generation_config={
                    "temperature": temperature,
                    "max_output_tokens": max_tokens,
                },
            )
            return response.text
        except Exception as e:
            print(f"Error generating text: {str(e)}")
            return ""

    async def generate_structured_chat(
        self, messages: List[Dict[str, str]], temperature: float = 0.7
    ) -> str:
        try:
            chat = self.model.start_chat(history=[])

            for message in messages:
                if message["role"] == "user":
                    response = await chat.send_message_async(
                        message["content"],
                        generation_config={"temperature": temperature},
                    )

            return response.text
        except Exception as e:
            print(f"Error in chat generation: {str(e)}")
            return ""

    async def generate_with_context(
        self, prompt: str, context: str, temperature: float = 0.7
    ) -> str:
        try:
            combined_prompt = f"Context: {context}\n\nPrompt: {prompt}"
            response = await self.model.generate_content_async(
                combined_prompt, generation_config={"temperature": temperature}
            )
            return response.text
        except Exception as e:
            print(f"Error generating with context: {str(e)}")
            return ""
