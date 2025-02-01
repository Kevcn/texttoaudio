"""
Middleware package for the Text to Audio API.
Contains middleware components for rate limiting and other functionality.
"""

from .rate_limiter import RateLimiter, rate_limit_middleware

__all__ = ['RateLimiter', 'rate_limit_middleware'] 