from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import tts
from .middleware.rate_limiter import RateLimiter, rate_limit_middleware
from starlette.middleware.base import BaseHTTPMiddleware
import uvicorn

app = FastAPI(
    title="Text to Audio API",
    description="API for converting text to audio using various TTS services",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend development server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure rate limiting
rate_limiter = RateLimiter(
    requests_per_minute=60,  # Allow 60 requests per minute per IP
    burst_limit=100  # Maximum burst size
)

# Start the cleanup task for rate limiting
@app.on_event("startup")
async def startup_event():
    rate_limiter.start_cleanup()

# Add rate limiting middleware
app.add_middleware(
    BaseHTTPMiddleware,
    dispatch=lambda request, call_next: rate_limit_middleware(request, call_next, rate_limiter)
)

# Include routers
app.include_router(tts.router)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Text to Audio API is running"}

@app.get("/api/v1/voices")
async def list_voices():
    """List available voices"""
    # TODO: Implement voice listing
    return {"voices": ["en-US-1", "en-US-2"]}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
