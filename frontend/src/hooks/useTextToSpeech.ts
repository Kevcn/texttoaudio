import { useState, useCallback, useEffect } from 'react';
import { textToSpeechService, TextToSpeechRequest, ApiError } from '../services/api';

interface UseTextToSpeechReturn {
  audioUrl: string | null;
  isLoading: boolean;
  error: string | null;
  convertText: (text: string, language: string) => Promise<void>;
  clearAudio: () => void;
}

export function useTextToSpeech(): UseTextToSpeechReturn {
  const [audioUrl, setAudioUrl] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Cleanup function for audio URL
  const clearAudio = useCallback(() => {
    if (audioUrl) {
      URL.revokeObjectURL(audioUrl);
      setAudioUrl(null);
    }
  }, [audioUrl]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      clearAudio();
    };
  }, [clearAudio]);

  const convertText = useCallback(async (text: string, language: string) => {
    try {
      setIsLoading(true);
      setError(null);
      
      // Clear previous audio if exists
      clearAudio();

      const request: TextToSpeechRequest = { text, language };
      const audioBlob = await textToSpeechService.convertTextToSpeech(request);
      const url = URL.createObjectURL(audioBlob);
      
      setAudioUrl(url);
    } catch (err) {
      const apiError = err as ApiError;
      setError(apiError.message || 'Failed to convert text to speech');
      setAudioUrl(null);
    } finally {
      setIsLoading(false);
    }
  }, [clearAudio]);

  return {
    audioUrl,
    isLoading,
    error,
    convertText,
    clearAudio,
  };
} 