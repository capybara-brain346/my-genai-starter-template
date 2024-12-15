import google.generativeai as genai
from typing import Optional, Union, BinaryIO
import speech_recognition as sr
from pydub import AudioSegment
import io
import os
import tempfile
from dotenv import load_dotenv

load_dotenv()


class GeminiAudioUtils:
    def __init__(self):
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        self.recognizer = sr.Recognizer()

    async def _convert_to_wav(
        self, audio_input: Union[str, bytes, BinaryIO], target_sample_rate: int = 16000
    ) -> str:
        try:
            temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")

            if isinstance(audio_input, str):
                audio = AudioSegment.from_file(audio_input)
            elif isinstance(audio_input, bytes):
                audio = AudioSegment.from_file(io.BytesIO(audio_input))
            elif isinstance(audio_input, BinaryIO):
                audio = AudioSegment.from_file(audio_input)
            else:
                raise ValueError("Unsupported audio input type")

            audio = audio.set_frame_rate(target_sample_rate)
            audio.export(temp_wav.name, format="wav")

            return temp_wav.name
        except Exception as e:
            raise ValueError(f"Error converting audio: {str(e)}")

    async def transcribe_audio(
        self, audio_input: Union[str, bytes, BinaryIO], language: str = "en-US"
    ) -> str:
        try:
            wav_path = await self._convert_to_wav(audio_input)

            with sr.AudioFile(wav_path) as source:
                audio = self.recognizer.record(source)
                transcript = self.recognizer.recognize_google(audio, language=language)

            os.unlink(wav_path)

            return transcript
        except Exception as e:
            print(f"Error transcribing audio: {str(e)}")
            return ""

    async def analyze_audio_content(
        self,
        audio_input: Union[str, bytes, BinaryIO],
        prompt: Optional[str] = None,
        language: str = "en-US",
        temperature: float = 0.7,
    ) -> str:
        try:
            transcript = await self.transcribe_audio(audio_input, language)

            if not transcript:
                return "Could not transcribe audio"

            default_prompt = (
                "Analyze the following audio transcript and provide insights:"
            )
            analysis_prompt = f"{prompt or default_prompt}\n\nTranscript: {transcript}"

            response = await self.model.generate_content_async(
                analysis_prompt, generation_config={"temperature": temperature}
            )
            return response.text
        except Exception as e:
            print(f"Error analyzing audio content: {str(e)}")
            return ""

    async def summarize_audio(
        self,
        audio_input: Union[str, bytes, BinaryIO],
        max_length: Optional[int] = None,
        language: str = "en-US",
        temperature: float = 0.7,
    ) -> str:
        try:
            transcript = await self.transcribe_audio(audio_input, language)

            if not transcript:
                return "Could not transcribe audio"

            length_constraint = f" in {max_length} words or less" if max_length else ""
            summary_prompt = f"Provide a concise summary of the following transcript{length_constraint}:\n\n{transcript}"

            response = await self.model.generate_content_async(
                summary_prompt, generation_config={"temperature": temperature}
            )
            return response.text
        except Exception as e:
            print(f"Error summarizing audio: {str(e)}")
            return ""
