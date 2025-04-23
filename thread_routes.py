from threads_auth import generate_login_url, exchange_code_for_token
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
import os
from dotenv import load_dotenv

load_dotenv()
router = APIRouter()

APP_ID = os.getenv("APP_ID")
REDIRECT_URI = os.getenv("REDIRECT_URI")
AUTH_URL = "https://www.facebook.com/v19.0/dialog/oauth"
SCOPES = "threads_basic,threads_content_publish"


@router.get("/")
async def home():
    return {"message": "Threads Automation FastAPI is running!"}


@router.get("/login")
async def login():
    url = generate_login_url()
    return RedirectResponse(url)


@router.get("/auth/callback")
async def callback(request: Request):
    code = request.query_params.get("code")
    if not code:
        return {"error": "Missing code in callback"}

    token_data = await exchange_code_for_token(code)
    return token_data
