import os
from pathlib import Path
from gtts import gTTS
from fastapi import HTTPException
import uuid
from datetime import datetime, timedelta

class TTSService:
    """
    Text-to-Speech Service using Google's TTS engine.
    
    This service handles the conversion of text to speech using Google's Text-to-Speech
    service (gTTS). It supports multiple languages and manages the storage of generated
    audio files.
    
    Attributes:
        output_dir (Path): Directory where generated audio files are stored
        supported_languages (dict): Dictionary of supported language codes and their names
        file_expiry_hours (int): Number of hours after which audio files are deleted
    """

    def __init__(self, file_expiry_hours: int = 24):
        """
        Initialize the TTS service.
        
        Creates the output directory if it doesn't exist and sets up supported languages.
        The output directory is used to store generated audio files.

        Args:
            file_expiry_hours (int): Number of hours to keep audio files before deletion
        """
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)
        self.file_expiry_hours = file_expiry_hours
        self.supported_languages = {
            "en": "English",
            "zh-cn": "Chinese (Mandarin)"
        }
        # Clean up old files on startup
        self._cleanup_old_files()

    async def convert_text_to_speech(self, text: str, lang: str = "en") -> str:
        """
        Convert text to speech using Google Text-to-Speech.
        
        This method validates the input text and language, then uses Google's TTS
        service to convert the text to speech. The generated audio is saved as an
        MP3 file with a unique filename.
        
        Args:
            text (str): The text to convert to speech. Must not be empty.
            lang (str, optional): The language code for the speech. Defaults to "en".
                                Must be one of the supported languages.
            
        Returns:
            str: The absolute path to the generated audio file.
            
        Raises:
            HTTPException: 
                - 400 status if the text is empty
                - 400 status if the language is not supported
                - 500 status if the conversion fails for any other reason
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
        if lang not in self.supported_languages:
            raise HTTPException(
                status_code=400,
                detail=f"Language '{lang}' is not supported. Supported languages: {list(self.supported_languages.keys())}"
            )

        try:
            # Create a unique filename
            filename = f"{uuid.uuid4()}.mp3"
            output_path = self.output_dir / filename

            # Convert text to speech
            tts = gTTS(text=text, lang=lang)
            tts.save(str(output_path))

            return str(output_path)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to convert text to speech: {str(e)}"
            )

    def get_available_languages(self) -> dict[str, str]:
        """
        Get list of available languages.
        
        Returns a dictionary mapping language codes to their human-readable names.
        This method is used to inform clients about which languages are supported
        by the service.
        
        Returns:
            dict[str, str]: Dictionary where keys are language codes (e.g., "en")
                           and values are language names (e.g., "English")
        """
        return self.supported_languages

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