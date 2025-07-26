from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from pubgapi import FastPubgChecker
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Set up rate limiter: 30 requests per minute per IP
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

# Optional: Allow CORS if you want to call from browser/other domains
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(RateLimitExceeded)
def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded. Try again later."}
    )

checker = FastPubgChecker()

class UserIdRequest(BaseModel):
    userid: str

@app.post("/check")
@limiter.limit("30/minute")
def check_single_userid(request: Request, body: UserIdRequest):
    result = checker.check_single_userid(body.userid)
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["error"])
    return result

@app.get("/uid/{userid}")
@limiter.limit("30/minute")
def check_userid_by_path(request: Request, userid: str):
    """Check PUBG user ID via URL path parameter"""
    result = checker.check_single_userid(userid)
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["error"])
    return result 