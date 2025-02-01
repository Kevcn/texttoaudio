# Text to Audio Backend

A FastAPI-based backend service for converting text to speech using Google Cloud Text-to-Speech.

## Features

- High-quality text-to-speech conversion using Google Cloud
- Support for multiple languages and voices
- Voice customization (pitch, speaking rate)
- RESTful API with OpenAPI documentation
- Comprehensive test coverage
- CORS support for frontend integration
- Automatic file cleanup (24-hour retention)
- Rate limiting protection against API abuse
- Continuous Integration and Deployment pipeline

## Requirements

- Python 3.8 or higher
- Virtual environment (recommended)
- Docker (for containerized deployment)
- Google Cloud API key with Text-to-Speech API enabled

## Google Cloud Setup

1. Create a Google Cloud project (if you haven't already):
   - Go to the [Google Cloud Console](https://console.cloud.google.com)
   - Click "Create Project" or select an existing project

2. Enable the Cloud Text-to-Speech API:
   - Go to [APIs & Services > Library](https://console.cloud.google.com/apis/library)
   - Search for "Cloud Text-to-Speech API"
   - Click "Enable"

3. Create an API key:
   - Go to [APIs & Services > Credentials](https://console.cloud.google.com/apis/credentials)
   - Click "Create Credentials" > "API key"
   - Copy your API key
   - (Optional) Restrict the API key to only the Text-to-Speech API for security

4. Set up the API key:
   - For local development: Create a `.env` file with your API key
   ```bash
   GOOGLE_CLOUD_API_KEY=your-api-key-here
   ```
   - For Docker: Pass the API key as an environment variable (see Docker section)

## Installation

1. Clone the repository and navigate to the backend directory:
```bash
cd backend
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install the package in development mode:
```bash
pip install -e .
```

5. Create a `.env` file from the example:
```bash
cp .env.example .env
```
Then edit the `.env` file with your API key and other configuration.

## Running the Server

### Local Development
Start the development server:
```bash
uvicorn app.main:app --reload
```

The server will be available at `http://localhost:8000`. If port 8000 is in use, you can specify a different port:
```bash
uvicorn app.main:app --reload --port 8002
```

### Docker
Build and run using Docker:
```bash
# Build the image
docker build -t text-to-audio-backend .

# Run the container with API key
docker run -d \
  -p 8000:8000 \
  -e GOOGLE_CLOUD_API_KEY=your-api-key-here \
  --name text-to-audio-backend \
  text-to-audio-backend
```

## CI/CD Pipeline

The project uses GitHub Actions for continuous integration and deployment.

### Continuous Integration

The CI pipeline (`backend-ci.yml`) includes:

- **Testing**: Runs the test suite on multiple Python versions (3.8-3.11)
  - Unit tests
  - Integration tests
  - Coverage reporting to Codecov

- **Linting**: Code quality checks
  - flake8 for style guide enforcement
  - black for code formatting
  - isort for import sorting
  - mypy for type checking

- **Security**: Security checks
  - bandit for security linting
  - safety for dependency vulnerability checks

### Continuous Deployment

The CD pipeline (`backend-cd.yml`) includes:

- **Docker Build**: Creates a Docker image for the application
- **Registry Push**: Pushes the image to a Docker registry
- **Deployment**: Deploys the application to production server
  - Pulls the latest image
  - Stops and removes the old container
  - Starts a new container with the latest version

### Required Secrets

The following secrets need to be set in GitHub repository settings:

- `DOCKER_REGISTRY`: Docker registry URL
- `DOCKER_USERNAME`: Docker registry username
- `DOCKER_PASSWORD`: Docker registry password
- `DEPLOY_KEY`: SSH private key for deployment
- `DEPLOY_HOST`: Production server hostname
- `DEPLOY_USER`: Production server username

## API Documentation

Once the server is running, you can access:
- OpenAPI documentation: `http://localhost:8000/docs`
- Alternative documentation: `http://localhost:8000/redoc`

### API Endpoints

- `GET /` - Health check endpoint
- `GET /api/v1/tts/languages` - List available languages
- `GET /api/v1/tts/voices` - List available voices
- `POST /api/v1/tts/convert` - Convert text to speech

### Voice Customization

The text-to-speech conversion supports several customization options:

- `language_code`: Language code (e.g., "en-US", "zh-CN")
- `voice_name`: Specific voice to use
- `speaking_rate`: Speaking rate (0.25 to 4.0)
- `pitch`: Pitch adjustment (-20.0 to 20.0)

### Example Request

Convert text to speech with customization:
```bash
curl -X POST "http://localhost:8000/api/v1/tts/convert" \
     -H "Content-Type: application/json" \
     -d '{
       "text": "Hello, world!",
       "language_code": "en-US",
       "voice_name": "en-US-Standard-A",
       "speaking_rate": 1.0,
       "pitch": 0.0
     }'
```

## File Management

The service includes automatic file management features:

- Generated audio files are stored in the `output` directory
- Files are automatically cleaned up after 24 hours
- Cleanup runs on service startup and before each new conversion
- Failed cleanups are logged but don't affect the service operation

You can customize the file retention period by modifying the `file_expiry_hours` parameter in `TTSService` initialization.

## Testing

Run the test suite:
```bash
python -m pytest tests/ -v
```

The test suite includes:
- API endpoint tests
- Text-to-speech conversion tests
- Error handling tests
- Language support tests
- File cleanup tests
- Rate limiting tests

## Project Structure

```
backend/
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   └── tts.py
│   ├── middleware/
│   │   ├── __init__.py
│   │   └── rate_limiter.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── tts_service.py
│   ├── __init__.py
│   └── main.py
├── tests/
│   ├── __init__.py
│   ├── test_main.py
│   ├── test_tts.py
│   └── test_rate_limiter.py
├── requirements.txt
├── pyproject.toml
└── README.md
```

## Development

### Adding New Features

1. Create new endpoints in `app/api/`
2. Add services in `app/services/`
3. Add corresponding tests in `tests/`
4. Update documentation as needed

### Running Tests During Development

For continuous testing during development:
```bash
python -m pytest tests/ -v --watch
```

## Error Handling

The API uses standard HTTP status codes:
- 200: Success
- 400: Bad Request (invalid input)
- 404: Not Found
- 429: Too Many Requests (rate limit exceeded)
- 500: Internal Server Error

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for your changes
5. Submit a pull request

## License

MIT License
