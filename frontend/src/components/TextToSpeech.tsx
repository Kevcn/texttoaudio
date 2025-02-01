import { useState, useEffect } from 'react';
import { Box, Button, Group, Textarea, Select, Alert, LoadingOverlay } from '@mantine/core';
import { useTextToSpeech } from '../hooks/useTextToSpeech';
import { textToSpeechService, Language } from '../services/api';

export function TextToSpeech() {
  const [text, setText] = useState('');
  const [language, setLanguage] = useState('en-GB');
  const [languages, setLanguages] = useState<Language[]>([]);
  const [fetchError, setFetchError] = useState<string | null>(null);
  const { audioUrl, isLoading, error: conversionError, convertText, clearAudio } = useTextToSpeech();

  useEffect(() => {
    // Fetch available languages when component mounts
    const fetchLanguages = async () => {
      try {
        setFetchError(null);
        const response = await textToSpeechService.getAvailableLanguages();
        setLanguages(response.languages);
      } catch (err) {
        setFetchError('Failed to fetch available languages');
        console.error('Failed to fetch languages:', err);
      }
    };
    fetchLanguages();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!text.trim()) return;
    await convertText(text, language);
  };

  const handleClear = () => {
    setText('');
    clearAudio();
  };

  return (
    <Box component="form" onSubmit={handleSubmit} maw={600} mx="auto" p="md" pos="relative">
      <LoadingOverlay visible={isLoading} overlayProps={{ blur: 2 }} />
      
      {fetchError && (
        <Alert color="red" title="Error" mb="md">
          {fetchError}
        </Alert>
      )}

      <Textarea
        label="Text to convert"
        placeholder="Enter text to convert to speech..."
        value={text}
        onChange={(e) => setText(e.currentTarget.value)}
        minRows={4}
        required
        mb="md"
        disabled={isLoading}
      />

      <Select
        label="Language"
        value={language}
        onChange={(value) => setLanguage(value || 'en-GB')}
        data={languages.map(lang => ({
          value: lang.code,
          label: lang.name
        }))}
        mb="md"
        disabled={isLoading || languages.length === 0}
      />

      <Group justify="space-between" mb="md">
        <Button type="submit" loading={isLoading} disabled={!text.trim()}>
          {isLoading ? 'Converting...' : 'Convert to Speech'}
        </Button>
        <Button variant="light" color="gray" onClick={handleClear} disabled={isLoading || (!text && !audioUrl)}>
          Clear
        </Button>
      </Group>

      {conversionError && (
        <Alert color="red" title="Conversion Error" mb="md">
          {conversionError}
        </Alert>
      )}

      {audioUrl && (
        <Box>
          <audio 
            controls 
            src={audioUrl} 
            style={{ width: '100%' }} 
            onError={() => setFetchError('Failed to load audio')}
          />
          <Button
            component="a"
            href={audioUrl}
            download="speech.mp3"
            variant="light"
            mt="sm"
            fullWidth
          >
            Download Audio
          </Button>
        </Box>
      )}
    </Box>
  );
} 