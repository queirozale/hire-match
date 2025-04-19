import os
from fastapi import APIRouter, Depends, HTTPException, Request
from authlib.integrations.starlette_client import OAuth
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
import logging
from fastapi.logger import logger
from fastapi.responses import JSONResponse
logging.basicConfig(level=logging.DEBUG)

load_dotenv()

router = APIRouter()

# Auth0 Configuration
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
AUTH0_CALLBACK_URL = os.getenv("AUTH0_CALLBACK_URL")
AUTH0_AUDIENCE = os.getenv("AUTH0_AUDIENCE")

oauth = OAuth()
oauth.register(
    name="auth0",
    client_id=AUTH0_CLIENT_ID,
    client_secret=AUTH0_CLIENT_SECRET,
    authorize_url=f"https://{AUTH0_DOMAIN}/authorize",
    authorize_params={
        "audience": AUTH0_AUDIENCE,  # Ensure this is correct!
        "response_type": "code",
        "scope": "openid profile email",  # Ensure profile & email are requested
    },
    access_token_url=f"https://{AUTH0_DOMAIN}/oauth/token",
    access_token_params=None,
    redirect_uri=AUTH0_CALLBACK_URL,
    client_kwargs={"scope": "openid profile email"},
)


# Redirect to Auth0 Login
@router.api_route("/login", methods=["GET", "POST"])
async def login(request: Request):
    return await oauth.auth0.authorize_redirect(request, AUTH0_CALLBACK_URL)

# Handle Auth0 Callback
@router.api_route("/auth/callback", methods=["GET", "POST"])
async def auth_callback(request: Request):
    try:
        token = await oauth.auth0.authorize_access_token(request)
        print(f"Token received: {token}")  # Debugging log

        user = token.get("userinfo")
        print(f"User info: {user}")  # Debugging log

        if not user:
            return JSONResponse(status_code=400, content={"error": "User not found in token"})

        return {"message": "Login successful", "user": user}

    except Exception as e:
        print(f"Error during authentication: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})


# Logout
@router.api_route("/logout", methods=["GET", "POST"])
async def logout():
    return RedirectResponse(url=f"https://{AUTH0_DOMAIN}/v2/logout?returnTo=http://localhost:8000")
