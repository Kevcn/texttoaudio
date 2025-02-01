import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { TextToSpeech } from '../TextToSpeech';
import { textToSpeechService } from '../../services/api';
import '@testing-library/jest-dom';

// Mock the text-to-speech service
jest.mock('../../services/api', () => ({
  textToSpeechService: {
    getAvailableLanguages: jest.fn(),
    convertTextToSpeech: jest.fn(),
  },
}));

describe('TextToSpeech Component', () => {
  beforeEach(() => {
    // Reset mocks before each test
    jest.clearAllMocks();
    
    // Mock the getAvailableLanguages response
    (textToSpeechService.getAvailableLanguages as jest.Mock).mockResolvedValue({
      languages: [
        { code: 'en', name: 'English' },
        { code: 'zh-cn', name: 'Chinese (Mandarin)' },
      ],
    });
  });

  it('renders without crashing', () => {
    render(<TextToSpeech />);
    expect(screen.getByLabelText(/text to convert/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/language/i)).toBeInTheDocument();
  });

  it('loads available languages on mount', async () => {
    render(<TextToSpeech />);
    await waitFor(() => {
      expect(textToSpeechService.getAvailableLanguages).toHaveBeenCalled();
    });
  });

  it('handles text input', () => {
    render(<TextToSpeech />);
    const input = screen.getByLabelText(/text to convert/i);
    fireEvent.change(input, { target: { value: 'Hello, world!' } });
    expect(input).toHaveValue('Hello, world!');
  });

  it('handles language selection', async () => {
    render(<TextToSpeech />);
    await waitFor(() => {
      expect(screen.getByLabelText(/language/i)).not.toBeDisabled();
    });
    
    const select = screen.getByLabelText(/language/i);
    fireEvent.change(select, { target: { value: 'zh-cn' } });
    expect(select).toHaveValue('zh-cn');
  });

  it('handles successful conversion', async () => {
    const mockBlob = new Blob(['audio-data'], { type: 'audio/mpeg' });
    (textToSpeechService.convertTextToSpeech as jest.Mock).mockResolvedValue(mockBlob);

    render(<TextToSpeech />);
    
    // Enter text
    fireEvent.change(screen.getByLabelText(/text to convert/i), {
      target: { value: 'Hello, world!' },
    });

    // Submit form
    fireEvent.click(screen.getByText(/convert to speech/i));

    await waitFor(() => {
      expect(textToSpeechService.convertTextToSpeech).toHaveBeenCalledWith({
        text: 'Hello, world!',
        language: 'en',
      });
    });
  });

  it('handles conversion error', async () => {
    const errorMessage = 'Failed to convert text to speech';
    (textToSpeechService.convertTextToSpeech as jest.Mock).mockRejectedValue({
      message: errorMessage,
    });

    render(<TextToSpeech />);
    
    // Enter text
    fireEvent.change(screen.getByLabelText(/text to convert/i), {
      target: { value: 'Hello, world!' },
    });

    // Submit form
    fireEvent.click(screen.getByText(/convert to speech/i));

    await waitFor(() => {
      expect(screen.getByText(errorMessage)).toBeInTheDocument();
    });
  });

  it('clears text and audio when clear button is clicked', async () => {
    const mockBlob = new Blob(['audio-data'], { type: 'audio/mpeg' });
    (textToSpeechService.convertTextToSpeech as jest.Mock).mockResolvedValue(mockBlob);

    render(<TextToSpeech />);
    
    // Enter text
    fireEvent.change(screen.getByLabelText(/text to convert/i), {
      target: { value: 'Hello, world!' },
    });

    // Submit and wait for conversion
    fireEvent.click(screen.getByText(/convert to speech/i));
    await waitFor(() => {
      expect(textToSpeechService.convertTextToSpeech).toHaveBeenCalled();
    });

    // Click clear button
    fireEvent.click(screen.getByText(/clear/i));

    // Verify text is cleared
    expect(screen.getByLabelText(/text to convert/i)).toHaveValue('');
  });
}); 