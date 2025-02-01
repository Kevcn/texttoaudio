# Text to Audio Backend

A FastAPI-based backend service for converting text to speech using Google's Text-to-Speech service.

## Features

- Convert text to speech in multiple languages
- Support for English and Chinese (Mandarin)
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

# Run the container
docker run -d -p 8000:8000 --name text-to-audio-backend text-to-audio-backend
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
- `POST /api/v1/tts/convert` - Convert text to speech
- `GET /api/v1/voices` - List available voices (TODO)

### Rate Limiting

The API implements rate limiting to prevent abuse:

- Default limit: 60 requests per minute per IP address
- Burst limit: 100 requests maximum
- Status code 429 is returned when rate limit is exceeded
- Limits are tracked separately for each IP address
- Rate limit counters reset automatically after one minute
- Old rate limit data is automatically cleaned up

### Example Request

Convert text to speech:
```bash
curl -X POST "http://localhost:8000/api/v1/tts/convert" \
     -H "Content-Type: application/json" \
     -d '{"text": "Hello, world!", "language": "en"}'
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
