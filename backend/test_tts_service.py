import asyncio
from app.services.tts_service import TTSService
import os

async def test_tts():
    print("Starting TTS service test...")
    
    try:
        # Initialize service
        print("Initializing TTS service...")
        service = TTSService()
        print("TTS service initialized successfully!")
        
        # Test getting languages
        print("\nTesting language listing...")
        languages = service.get_available_languages()
        print(f"Available languages: {languages}")
        assert len(languages) == 2, "Should only support English and Chinese"
        assert "en-GB" in languages, "Should support English (Great Britain)"
        assert "zh-CN" in languages, "Should support Chinese (Mandarin)"
        
        # Test getting voices
        print("\nTesting voice listing...")
        voices = service.get_voices()
        print(f"Available voices: {voices}")
        assert "en-GB" in voices, "Should have English voices"
        assert "zh-CN" in voices, "Should have Chinese voices"
        
        # Test text-to-speech conversion for English
        print("\nTesting English text-to-speech conversion...")
        en_text = "Hello, this is a test of the text-to-speech service."
        en_output_path = await service.convert_text_to_speech(
            text=en_text,
            language_code="en-GB",
            voice_name="en-GB-Journey-D"
        )
        print(f"English audio file generated at: {en_output_path}")
        
        # Test text-to-speech conversion for Chinese
        print("\nTesting Chinese text-to-speech conversion...")
        zh_text = "你好，这是文字转语音服务的测试。"
        zh_output_path = await service.convert_text_to_speech(
            text=zh_text,
            language_code="zh-CN",
            voice_name="cmn-CN-Standard-A"
        )
        print(f"Chinese audio file generated at: {zh_output_path}")
        
        # Test invalid language
        print("\nTesting invalid language (should fail)...")
        try:
            await service.convert_text_to_speech(
                text="Bonjour",
                language_code="fr-FR"
            )
            print("Error: Should have rejected French language")
            raise AssertionError("Should have rejected French language")
        except Exception as e:
            print(f"Successfully rejected invalid language: {str(e)}")
        
        # Test invalid voice
        print("\nTesting invalid voice (should fail)...")
        try:
            await service.convert_text_to_speech(
                text="Hello",
                language_code="en-US",
                voice_name="en-US-Invalid-Voice"
            )
            print("Error: Should have rejected invalid voice")
            raise AssertionError("Should have rejected invalid voice")
        except Exception as e:
            print(f"Successfully rejected invalid voice: {str(e)}")
        
        # Verify files exist
        print("\nVerifying generated files...")
        for path in [en_output_path, zh_output_path]:
            if os.path.exists(path):
                file_size = os.path.getsize(path)
                print(f"File {path} created successfully! Size: {file_size} bytes")
            else:
                print(f"Error: Audio file {path} was not created!")
                raise AssertionError(f"Audio file {path} was not created")
        
        print("\nAll tests completed successfully!")
            
    except Exception as e:
        print(f"Error during test: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(test_tts()) 