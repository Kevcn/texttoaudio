# Text to Audio Converter

A modern web application that converts text to speech, supporting multiple languages including English and Chinese Mandarin.

## Features

- Text to speech conversion with multiple language support
- Clean and responsive web interface
- Real-time audio playback
- Download capability for generated audio
- Error handling and user feedback
- Resource cleanup and optimization
- Cross-browser compatibility
- Asynchronous processing for longer texts

## Tech Stack

### Backend
- Python 3.8+
- FastAPI - Modern web framework for building APIs
- Uvicorn - Lightning-fast ASGI server
- Text-to-Speech service integration
- CORS middleware for secure frontend communication

### Frontend
- React 18+ - UI library
- TypeScript - Type-safe JavaScript
- Mantine UI - Modern React component library
- Vite - Next generation frontend tooling
- Axios - Promise based HTTP client

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn
- Git

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd textToAudio
```

2. Set up the backend:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

3. Set up the frontend:
```bash
cd frontend
npm install
```

### Running the Application

1. Start the backend server:
```bash
cd backend
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
uvicorn app.main:app --reload
```
The backend will be available at http://localhost:8000

2. Start the frontend development server:
```bash
cd frontend
npm run dev
```
The frontend will be available at http://localhost:5173

### Environment Variables

Backend:
- `TTS_API_KEY` - API key for the text-to-speech service (if required)
- `ENVIRONMENT` - Development/production environment setting
- `MAX_TEXT_LENGTH` - Maximum allowed text length (default: 1000)

Frontend:
- `VITE_API_URL` - Backend API URL (default: http://localhost:8000)

## Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

### End-to-End Tests
```bash
npm run test:e2e
```

## API Documentation

See [API.md](docs/API.md) for detailed API documentation.

## Project Structure

```
textToAudio/
├── backend/
│   ├── app/
│   │   ├── api/          # API routes and endpoints
│   │   ├── services/     # Business logic and external services
│   │   └── main.py      # Application entry point
│   ├── tests/           # Test files
│   ├── requirements.txt # Python dependencies
│   └── pyproject.toml  # Python project configuration
├── frontend/
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── services/    # API services and utilities
│   │   └── hooks/      # Custom React hooks
│   ├── package.json    # Node.js dependencies
│   └── vite.config.ts  # Vite configuration
└── docs/
    └── API.md         # API documentation
```

## Troubleshooting

### Common Issues

1. Backend Import Error:
```
ModuleNotFoundError: No module named 'app'
```
Solution: Ensure you're running the server from the backend directory and PYTHONPATH includes the current directory.

2. Frontend API Connection Error:
```
Failed to fetch languages
```
Solution: Verify the backend server is running and CORS is properly configured.

3. Audio Playback Issues:
- Clear browser cache
- Check browser console for errors
- Verify audio format compatibility

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guide for Python code
- Use ESLint and Prettier for JavaScript/TypeScript code
- Write tests for new features
- Update documentation as needed

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- FastAPI for the excellent web framework
- Mantine UI for the beautiful components
- All contributors who have helped shape this project 