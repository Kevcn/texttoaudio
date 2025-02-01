# API Documentation

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

Currently, the API does not require authentication. However, rate limiting is applied to prevent abuse.

## Common Headers

All requests should include:
```http
Content-Type: application/json
Accept: application/json
```

## Endpoints

### Health Check

```http
GET /
```

Returns the health status of the API.

#### Request Example
```bash
curl http://localhost:8000/api/v1/
```

#### Response

```json
{
  "status": "healthy",
  "message": "Text to Audio API is running"
}
```

### Get Available Languages

```http
GET /tts/languages
```

Returns a list of available languages for text-to-speech conversion.

#### Request Example
```bash
curl http://localhost:8000/api/v1/tts/languages
```

#### Response

```json
{
  "languages": [
    {
      "code": "en",
      "name": "English"
    },
    {
      "code": "zh-cn",
      "name": "Chinese (Mandarin)"
    }
  ]
}
```

#### Response Headers
```http
Content-Type: application/json
Cache-Control: max-age=3600
```

### Convert Text to Speech

```http
POST /tts/convert
```

Converts text to speech in the specified language.

#### Request Body

```json
{
  "text": "string",
  "language": "string"
}
```

| Parameter | Type | Description | Required | Constraints |
|-----------|------|-------------|----------|-------------|
| text | string | The text to convert to speech | Yes | Max 1000 chars |
| language | string | The language code (e.g., "en", "zh-cn") | Yes | Must be supported |

#### Request Example
```bash
curl -X POST http://localhost:8000/api/v1/tts/convert \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello, world!", "language": "en"}'
```

#### Response

Returns an audio file (MP3 format) with the following headers:

```http
Content-Type: audio/mpeg
Content-Disposition: attachment; filename="speech.mp3"
Content-Length: <size-in-bytes>
Cache-Control: no-cache
```

#### Error Responses

##### 400 Bad Request

```json
{
  "detail": "Text cannot be empty"
}
```

Possible causes:
- Empty text field
- Text exceeds maximum length
- Invalid JSON format

##### 404 Not Found

```json
{
  "detail": "Language not supported"
}
```

Possible causes:
- Unsupported language code
- Language service unavailable

##### 500 Internal Server Error

```json
{
  "detail": "Failed to convert text to speech"
}
```

Possible causes:
- TTS service error
- Server configuration issue
- Resource constraints

## Error Handling

All endpoints follow a consistent error response format:

```json
{
  "detail": "Error message description"
}
```

Common HTTP status codes:

- 200: Success
- 400: Bad Request (invalid input)
- 404: Not Found
- 429: Too Many Requests
- 500: Internal Server Error

## Rate Limiting

The API implements the following rate limits:

- Maximum text length: 1000 characters
- Maximum requests per minute: 60
- Maximum concurrent requests: 10

Rate limit headers are included in responses:
```http
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 59
X-RateLimit-Reset: 1640995200
```

## Performance Considerations

- Large text conversion may take longer to process
- Audio files are temporarily cached for 5 minutes
- Consider implementing client-side caching for frequently used conversions
- Use compression for larger audio files

## CORS

The API supports CORS for the frontend application running on `http://localhost:5173`. For other origins, please contact the API administrator.

Cross-origin headers:
```http
Access-Control-Allow-Origin: http://localhost:5173
Access-Control-Allow-Methods: GET, POST, OPTIONS
Access-Control-Allow-Headers: Content-Type
Access-Control-Allow-Credentials: true
```

## API Versioning

The API uses URL versioning (v1). Future versions will be available at `/api/v2`, `/api/v3`, etc.

Version changelog:
- v1: Initial release with basic TTS functionality
- v2: (Planned) Additional voice options and formatting support

## Best Practices

1. Always check the language availability before making conversion requests
2. Handle errors appropriately in your client application
3. Clean up audio resources when they're no longer needed
4. Include appropriate error handling for network issues
5. Implement retry logic for failed requests
6. Cache frequently used conversions
7. Monitor rate limits and implement backoff strategies

## Support

For API support or to report issues:
1. Open an issue in the GitHub repository
2. Contact the development team
3. Check the troubleshooting guide in README.md 