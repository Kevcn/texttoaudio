import { MantineProvider, Container, Title, Paper } from '@mantine/core';
import { TextToSpeech } from './components/TextToSpeech';
import '@mantine/core/styles.css';

function App() {
  return (
    <MantineProvider>
      <Container size="lg" py="xl">
        <Paper shadow="sm" p="xl" withBorder>
          <Title order={1} ta="center" mb="xl">
            Text to Speech Converter
          </Title>
          <TextToSpeech />
        </Paper>
      </Container>
    </MantineProvider>
  );
}

export default App;
