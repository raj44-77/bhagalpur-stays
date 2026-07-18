"""Rate limiting middleware with account lockout"""
from fastapi import Request, HTTPException
from collections import defaultdict
import time

request_log = defaultdict(list)
login_attempts = defaultdict(lambda: {"count": 0, "locked_until": 0})

RATE_LIMITS = {
    "/api/auth/login": {"max": 5, "window": 60},
    "/api/auth/signup": {"max": 3, "window": 60},
    "/api/auth/forgot-password": {"max": 3, "window": 300},
}

MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_DURATION = 900  # 15 minutes


async def rate_limit_middleware(request: Request, call_next):
    path = request.url.path
    limit = RATE_LIMITS.get(path)

    if limit:
        client_ip = request.client.host
        now = time.time()

        # Check account lockout for login
        if path == "/api/auth/login":
            lock_data = login_attempts[client_ip]
            if lock_data["locked_until"] > now:
                remaining = int(lock_data["locked_until"] - now)
                raise HTTPException(
                    status_code=429,
                    detail=f"Account temporarily locked. Try again in {remaining} seconds."
                )

        # Rate limiting
        window_start = now - limit["window"]
        request_log[client_ip] = [t for t in request_log[client_ip] if t > window_start]

        if len(request_log[client_ip]) >= limit["max"]:
            raise HTTPException(status_code=429, detail="Too many requests. Please try again later.")

        request_log[client_ip].append(now)

    response = await call_next(request)
    return response


def record_failed_login(ip: str):
    """Record a failed login attempt"""
    now = time.time()
    lock_data = login_attempts[ip]
    
    if lock_data["locked_until"] > now:
        return  # Already locked
    
    lock_data["count"] += 1
    
    if lock_data["count"] >= MAX_LOGIN_ATTEMPTS:
        lock_data["locked_until"] = now + LOCKOUT_DURATION
        lock_data["count"] = 0


def reset_login_attempts(ip: str):
    """Reset login attempts on successful login"""
    login_attempts[ip] = {"count": 0, "locked_until": 0}