import os
import httpx
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse

router = APIRouter(prefix="/auth", tags=["auth"])

CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
CLIENT_SECRET = os.getenv("TWITCH_CLIENT_SECRET")
REDIRECT_URI = os.getenv("TWITCH_REDIRECT_URI")
SCOPES = "chat:read chat:edit moderation:manage moderator:manage:banned_users"

# Twitch OAuth 認証ページにリダイレクト
@router.get("/login")
async def twitch_login():
    auth_url = (
        f"https://id.twitch.tv/oauth2/authorize"
        f"?response_type=code"
        f"&client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope={SCOPES}"
    )
    return RedirectResponse(auth_url)

# OAuth認証のコールバック
@router.get("/callback")
async def twitch_callback(request: Request):
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Missing code")

    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            "https://id.twitch.tv/oauth2/token",
            data={
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": REDIRECT_URI,
            },
        )
    if token_response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to get access token")
    
    tokens = token_response.json()
    access_token = tokens["access_token"]
    refresh_token = tokens["refresh_token"]

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Client-ID": CLIENT_ID
    }
    async with httpx.AsyncClient() as client:
        user_response = await client.get(
            "https://api.twitch.tv/helix/users",
            headers=headers
        )
    if user_response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to get user info")
    
    user_info = user_response.json()["data"][0]
    streamer_id = user_info["id"]
    streamer_login = user_info["login"]

    # TODO: ユーザー情報をDBに保存

    return {
        "streamer_id": streamer_id,
        "streamer_login": streamer_login,
        "access_token": access_token,
        "refresh_token": refresh_token
    }
    