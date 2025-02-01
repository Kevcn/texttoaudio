from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import time
from typing import Dict, Tuple
import asyncio

class RateLimiter:
    def __init__(
        self,
        requests_per_minute: int = 60,
        burst_limit: int = 100
    ):
        self.requests_per_minute = requests_per_minute
        self.burst_limit = burst_limit
        self.clients: Dict[str, Tuple[float, int]] = {}
        self._cleanup_task = None

    async def _cleanup_old_clients(self) -> None:
        """Periodically clean up old client records"""
        while True:
            current_time = time.time()
            # Remove clients that haven't made requests in the last minute
            self.clients = {
                ip: data
                for ip, data in self.clients.items()
                if current_time - data[0] < 60
            }
            await asyncio.sleep(60)  # Run cleanup every minute

    def start_cleanup(self) -> None:
        """Start the cleanup task"""
        if self._cleanup_task is None:
            self._cleanup_task = asyncio.create_task(self._cleanup_old_clients())

    async def is_rate_limited(self, ip: str) -> bool:
        """Check if a client has exceeded their rate limit"""
        current_time = time.time()
        
        if ip not in self.clients:
            # First request from this IP
            self.clients[ip] = (current_time, 1)
            return False
        
        last_request_time, request_count = self.clients[ip]
        time_passed = current_time - last_request_time
        
        # Reset counter if a minute has passed
        if time_passed >= 60:
            self.clients[ip] = (current_time, 1)
            return False
        
        # Calculate the allowed requests based on time passed
        allowed_requests = min(
            self.burst_limit,
            int(self.requests_per_minute * (time_passed / 60)) + 1
        )
        
        if request_count >= allowed_requests:
            return True
        
        # Increment request count
        self.clients[ip] = (last_request_time, request_count + 1)
        return False

async def rate_limit_middleware(
    request: Request,
    call_next,
    limiter: RateLimiter
):
    """Middleware function to apply rate limiting"""
    # Get client IP
    client_ip = request.client.host if request.client else "unknown"
    
    # Check rate limit
    if await limiter.is_rate_limited(client_ip):
        return JSONResponse(
            status_code=429,
            content={
                "detail": "Too many requests. Please try again later."
            }
        )
    
    # Process the request if not rate limited
    response = await call_next(request)
    return response 