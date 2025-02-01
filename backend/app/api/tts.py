from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from app.services.tts_service import tts_service
import os

router = APIRouter(prefix="/api/v1/tts", tags=["text-to-speech"])

class TextToSpeechRequest(BaseModel):
    """
    Request model for text-to-speech conversion.
    
    Attributes:
        text (str): The text to convert to speech. Must not be empty.
        language (str): The language code for the speech. Defaults to "en".
                       Must be one of the supported languages.
    """
    text: str
    language: str = "en"

class LanguageInfo(BaseModel):
    """
    Model representing a supported language.
    
    Attributes:
        code (str): The language code (e.g., "en", "zh-cn")
        name (str): The human-readable language name (e.g., "English", "Chinese (Mandarin)")
    """
    code: str
    name: str

@router.post("/convert")
async def convert_text_to_speech(request: TextToSpeechRequest):
    """
    Convert text to speech and return the audio file.
    
    This endpoint accepts text and a language code, converts the text to speech
    using Google's TTS service, and returns the audio as an MP3 file.
    
    Args:
        request (TextToSpeechRequest): The request containing text and language.
    
    Returns:
        FileResponse: The audio file in MP3 format.
    
    Raises:
        HTTPException: 
            - 400: If the text is empty or the language is not supported
            - 500: If the conversion fails for any other reason
    
    Example:
        ```
        POST /api/v1/tts/convert
        {
            "text": "Hello, world!",
            "language": "en"
        }
        ```
    """
    try:
        # Convert text to speech
        audio_path = await tts_service.convert_text_to_speech(
            text=request.text,
            lang=request.language
        )

        # Return the audio file
        return FileResponse(
            audio_path,
            media_type="audio/mpeg",
            filename="speech.mp3"
        )
    except HTTPException as he:
        # Re-raise HTTP exceptions as is
        raise he
    except Exception as e:
        # Convert other exceptions to 500 errors
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/languages")
async def get_languages():
    """
    Get list of available languages.
    
    Returns a list of supported languages with their codes and names.
    This endpoint is useful for clients to determine which languages
    are available for text-to-speech conversion.
    
    Returns:
        dict: A dictionary containing a list of language objects, each with:
            - code (str): The language code
            - name (str): The human-readable language name
    
    Example Response:
        ```json
        {
            "languages": [
                {"code": "en", "name": "English"},
                {"code": "zh-cn", "name": "Chinese (Mandarin)"}
            ]
        }
        ```
    """
    languages = tts_service.get_available_languages()
    return {
        "languages": [
            {"code": code, "name": name}
            for code, name in languages.items()
        ]
    } 