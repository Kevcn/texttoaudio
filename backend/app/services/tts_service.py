import os
from pathlib import Path
from fastapi import HTTPException
import uuid
from datetime import datetime, timedelta
import requests
from typing import Dict, List, Optional
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

class TTSService:
    """
    Text-to-Speech Service using Google Cloud Text-to-Speech.
    
    This service handles the conversion of text to speech using Google Cloud's
    Text-to-Speech service. It supports English and Chinese Mandarin, and manages
    the storage of generated audio files.
    
    Attributes:
        output_dir (Path): Directory where generated audio files are stored
        api_key (str): Google Cloud API key
        supported_languages (dict): Dictionary of supported language codes and their names
        available_voices (dict): Dictionary of available voices by language code
        file_expiry_hours (int): Number of hours after which audio files are deleted
    """

    # Predefined supported languages and voices
    SUPPORTED_LANGUAGES = {
        "en-GB": "English (Great Britain)",
        "zh-CN": "Chinese (Mandarin)"
    }

    # Predefined voices for supported languages
    AVAILABLE_VOICES = {
        "en-GB": [
            {"name": "en-GB-Journey-D", "gender": "FEMALE", "natural": True},
            {"name": "en-GB-Neural2-A", "gender": "FEMALE", "natural": True},
            {"name": "en-GB-Neural2-B", "gender": "MALE", "natural": True},
            {"name": "en-GB-Neural2-C", "gender": "FEMALE", "natural": True},
            {"name": "en-GB-Neural2-D", "gender": "MALE", "natural": True},
            {"name": "en-GB-Neural2-F", "gender": "FEMALE", "natural": True}
        ],
        "zh-CN": [
            {"name": "cmn-CN-Standard-A", "gender": "FEMALE", "natural": False},
            {"name": "cmn-CN-Standard-B", "gender": "MALE", "natural": False},
            {"name": "cmn-CN-Standard-C", "gender": "MALE", "natural": False},
            {"name": "cmn-CN-Standard-D", "gender": "FEMALE", "natural": False}
        ]
    }

    def __init__(self, file_expiry_hours: int = 24):
        """
        Initialize the TTS service.
        
        Creates the output directory if it doesn't exist.

        Args:
            file_expiry_hours (int): Number of hours to keep audio files before deletion
        """
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)
        self.file_expiry_hours = file_expiry_hours
        
        # Get API key from environment
        self.api_key = os.getenv("GOOGLE_CLOUD_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_CLOUD_API_KEY environment variable is not set")
        
        # Base URL for Google Cloud Text-to-Speech API
        self.base_url = "https://texttospeech.googleapis.com/v1"
        
        # Clean up old files on startup
        self._cleanup_old_files()

    async def convert_text_to_speech(
        self,
        text: str,
        language_code: str = "en-GB",
        voice_name: Optional[str] = None,
        speaking_rate: float = 1.0,
        pitch: float = 0.0
    ) -> str:
        """
        Convert text to speech using Google Cloud Text-to-Speech.
        
        Args:
            text (str): The text to convert to speech
            language_code (str): The language code (en-GB or zh-CN)
            voice_name (str, optional): Specific voice to use
            speaking_rate (float): Speaking rate, between 0.25 and 4.0
            pitch (float): Pitch adjustment, between -20.0 and 20.0
            
        Returns:
            str: Path to the generated audio file
            
        Raises:
            HTTPException: If the conversion fails or parameters are invalid
        """
        # Clean up old files before generating new ones
        self._cleanup_old_files()

        # Validate text
        if not text or not text.strip():
            raise HTTPException(
                status_code=400,
                detail="Text cannot be empty"
            )

        # Validate language
        if language_code not in self.SUPPORTED_LANGUAGES:
            raise HTTPException(
                status_code=400,
                detail=f"Language '{language_code}' is not supported. Supported languages: {list(self.SUPPORTED_LANGUAGES.keys())}"
            )

        try:
            # Select voice
            if voice_name is None:
                # Use the first available voice for the language
                voice_name = self.AVAILABLE_VOICES[language_code][0]["name"]
            else:
                # Validate voice name
                valid_voices = [v["name"] for v in self.AVAILABLE_VOICES[language_code]]
                if voice_name not in valid_voices:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Voice '{voice_name}' is not valid for language '{language_code}'"
                    )

            # Prepare request payload
            payload = {
                "input": {"text": text},
                "voice": {
                    "languageCode": language_code,
                    "name": voice_name
                },
                "audioConfig": {
                    "audioEncoding": "MP3",
                    "speakingRate": speaking_rate,
                    "pitch": pitch
                }
            }

            # Make request to Google Cloud TTS API
            url = f"{self.base_url}/text:synthesize?key={self.api_key}"
            response = requests.post(url, json=payload)
            
            if response.status_code != 200:
                raise Exception(f"Failed to synthesize speech: {response.text}")
            
            # Get audio content from response
            audio_content = response.json().get("audioContent")
            if not audio_content:
                raise Exception("No audio content in response")

            # Generate unique filename
            filename = f"{uuid.uuid4()}.mp3"
            output_path = self.output_dir / filename

            # Write the audio content to file
            import base64
            with open(output_path, "wb") as out:
                out.write(base64.b64decode(audio_content))

            return str(output_path)

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to convert text to speech: {str(e)}"
            )

    def get_available_languages(self) -> Dict[str, str]:
        """
        Get list of available languages.
        
        Returns:
            dict[str, str]: Dictionary mapping language codes to their names
        """
        return self.SUPPORTED_LANGUAGES

    def get_voices(self, language_code: Optional[str] = None) -> Dict[str, List[Dict]]:
        """
        Get available voices, optionally filtered by language code.
        
        Args:
            language_code (str, optional): Filter voices by language code
            
        Returns:
            dict: Dictionary of available voices by language code
        """
        if language_code:
            if language_code not in self.AVAILABLE_VOICES:
                raise HTTPException(
                    status_code=400,
                    detail=f"Language code '{language_code}' not found"
                )
            return {language_code: self.AVAILABLE_VOICES[language_code]}
        return self.AVAILABLE_VOICES

    def _cleanup_old_files(self) -> None:
        """
        Clean up audio files older than file_expiry_hours.
        
        This method is called automatically before generating new files and on service startup.
        It helps prevent disk space issues by removing old, unused audio files.
        """
        try:
            current_time = datetime.now()
            expiry_time = current_time - timedelta(hours=self.file_expiry_hours)
            
            for file_path in self.output_dir.glob("*.mp3"):
                # Get file modification time
                mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                
                # Remove file if it's older than expiry time
                if mtime < expiry_time:
                    try:
                        file_path.unlink()
                    except OSError:
                        # Log error but continue with other files
                        print(f"Failed to delete expired file: {file_path}")
        except Exception as e:
            # Log error but don't raise exception as this is a background task
            print(f"Error during file cleanup: {str(e)}")

# Create a singleton instance
tts_service = TTSService() 