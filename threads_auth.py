import os
import httpx
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

# ✅ Updated URLs for Threads API
AUTH_BASE_URL = "https://www.threads.net/oauth/authorize"
TOKEN_URL = "https://graph.threads.net/oauth/access_token"
LONG_LIVED_URL = "https://graph.threads.net/oauth/access_token"

# ✅ Expanded scopes based on official sample (you can reduce if needed)
SCOPES = "threads_basic,threads_content_publish"


def generate_login_url(state="123"):
    return (
        f"{AUTH_BASE_URL}?"
        f"client_id={APP_ID}&"
        f"redirect_uri={REDIRECT_URI}&"
        f"scope={SCOPES.replace(',', '%2C')}&"
        f"response_type=code&"
        f"state={state}"
    )


async def exchange_code_for_token(code: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(TOKEN_URL, data={
            "client_id": APP_ID,
            "client_secret": APP_SECRET,
            "redirect_uri": REDIRECT_URI,
            "code": code,
            "grant_type": "authorization_code"
        }, headers={
            "Content-Type": "application/x-www-form-urlencoded"
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


async def post_and_publish_thread(access_token: str, text: str, image_url: str = None):
    # Step 1: Create the container
    post_url = "https://graph.threads.net/me/threads"
    payload = {
        "text": text,
    }

    if image_url:
        payload["media_type"] = "IMAGE"
        payload["image_url"] = image_url

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient() as client:
        post_response = await client.post(post_url, json=payload, headers=headers)

    if post_response.status_code != 200:
        return {"error": "Failed to create post", "details": post_response.text}

    creation_id = post_response.json().get("id")

    # Step 2: Publish the thread
    publish_url = "https://graph.threads.net/me/threads_publish"
    publish_payload = {"creation_id": creation_id}

    async with httpx.AsyncClient() as client:
        publish_response = await client.post(publish_url, json=publish_payload, headers=headers)

    if publish_response.status_code != 200:
        return {"error": "Failed to publish thread", "details": publish_response.text}

    return {
        "status_code": publish_response.status_code,
        "thread_id": publish_response.json().get("id"),
        "creation_id": creation_id
    }
