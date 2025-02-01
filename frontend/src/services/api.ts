import axios, { AxiosError } from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/v1';

export interface TextToSpeechRequest {
  text: string;
  language_code: string;
  voice_name?: string;
  speaking_rate?: number;
  pitch?: number;
}

export interface Language {
  code: string;
  name: string;
}

export interface LanguageResponse {
  languages: Language[];
}

export interface ApiError {
  message: string;
  status?: number;
}

const api = axios.create({
  baseURL: API_BASE_URL,
  responseType: 'json',
});

// Error handling helper
const handleApiError = (error: unknown): never => {
  if (axios.isAxiosError(error)) {
    const axiosError = error as AxiosError<{ detail: string }>;
    throw {
      message: axiosError.response?.data?.detail || axiosError.message,
      status: axiosError.response?.status
    } as ApiError;
  }
  throw {
    message: error instanceof Error ? error.message : 'An unknown error occurred',
  } as ApiError;
};

export const textToSpeechService = {
  async convertTextToSpeech(request: TextToSpeechRequest): Promise<Blob> {
    try {
      const response = await api.post('/tts/convert', request, {
        responseType: 'blob',
      });
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async getAvailableLanguages(): Promise<LanguageResponse> {
    try {
      const response = await api.get<LanguageResponse>('/tts/languages');
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },
}; 