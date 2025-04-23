import os
import httpx
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

AUTH_BASE_URL = "https://www.facebook.com/v19.0/dialog/oauth"
TOKEN_URL = "https://graph.facebook.com/v19.0/oauth/access_token"
LONG_LIVED_URL = "https://graph.facebook.com/v19.0/oauth/access_token"

SCOPES = "threads_basic%2Cthreads_content_publish"


def generate_login_url(state="123"):
    return (
        f"{AUTH_BASE_URL}?"
        f"client_id={APP_ID}&"
        f"redirect_uri={REDIRECT_URI}&"
        f"scope={SCOPES}&"
        f"response_type=code&"
        f"state={state}"
    )


async def exchange_code_for_token(code: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(TOKEN_URL, params={
            "client_id": APP_ID,
            "redirect_uri": REDIRECT_URI,
            "client_secret": APP_SECRET,
            "code": code
        })

    if response.status_code != 200:
        return {"error": "Failed to exchange code", "details": response.text}

    return response.json()


async def exchange_for_long_lived_token(short_token: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(LONG_LIVED_URL, params={
            "grant_type": "fb_exchange_token",
            "client_id": APP_ID,
            "client_secret": APP_SECRET,
            "fb_exchange_token": short_token
        })

    if response.status_code != 200:
        return {"error": "Failed to get long-lived token", "details": response.text}

    return response.json()
