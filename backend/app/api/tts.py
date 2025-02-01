from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from app.services.tts_service import tts_service
import os

router = APIRouter(prefix="/api/v1/tts", tags=["text-to-speech"])

class TextToSpeechRequest(BaseModel):
    """
    Request model for text-to-speech conversion.
    
    Attributes:
        text (str): The text to convert to speech (required)
        language_code (str): The language code (e.g., "en-US", defaults to "en-US")
        voice_name (str, optional): Specific voice to use
        speaking_rate (float): Speaking rate, between 0.25 and 4.0
        pitch (float): Pitch adjustment, between -20.0 and 20.0
    """
    text: str = Field(..., description="Text to convert to speech")
    language_code: str = Field(default="en-US", description="Language code (e.g., en-US)")
    voice_name: Optional[str] = Field(None, description="Specific voice to use")
    speaking_rate: float = Field(
        default=1.0,
        ge=0.25,
        le=4.0,
        description="Speaking rate (0.25 to 4.0)"
    )
    pitch: float = Field(
        default=0.0,
        ge=-20.0,
        le=20.0,
        description="Pitch adjustment (-20.0 to 20.0)"
    )

class LanguageInfo(BaseModel):
    """
    Language information model.
    
    Attributes:
        code (str): Language code
        name (str): Human-readable language name
    """
    code: str
    name: str

class VoiceInfo(BaseModel):
    """
    Voice information model.
    
    Attributes:
        name (str): Voice name
        gender (str): Voice gender
        natural (bool): Whether the voice is natural or synthetic
    """
    name: str
    gender: str
    natural: bool

@router.post("/convert")
async def convert_text_to_speech(request: TextToSpeechRequest):
    """
    Convert text to speech using Google Cloud Text-to-Speech.
    
    Args:
        request (TextToSpeechRequest): The conversion request parameters
        
    Returns:
        FileResponse: The generated audio file
        
    Raises:
        HTTPException: If conversion fails or parameters are invalid
    """
    try:
        output_path = await tts_service.convert_text_to_speech(
            text=request.text,
            language_code=request.language_code,
            voice_name=request.voice_name,
            speaking_rate=request.speaking_rate,
            pitch=request.pitch
        )
        
        return FileResponse(
            output_path,
            media_type="audio/mpeg",
            filename=f"speech_{request.language_code}.mp3"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to convert text to speech: {str(e)}"
        )

@router.get("/languages")
async def get_languages():
    """
    Get list of available languages.
    
    Returns:
        dict: List of supported languages with their codes and names
    """
    languages = tts_service.get_available_languages()
    return {
        "languages": [
            LanguageInfo(code=code, name=name)
            for code, name in languages.items()
        ]
    }

@router.get("/voices")
async def get_voices(language_code: Optional[str] = None):
    """
    Get available voices, optionally filtered by language code.
    
    Args:
        language_code (str, optional): Filter voices by language code
        
    Returns:
        dict: Dictionary of available voices by language code
    """
    try:
        voices = tts_service.get_voices(language_code)
        return {"voices": voices}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get voices: {str(e)}"
        ) 