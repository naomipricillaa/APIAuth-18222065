from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse
from app.config import settings
from app.database import supabase 
import httpx

router = APIRouter()

# Google OAuth URLs
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"

@router.get("/login")
def login_with_google():
    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": settings.CALLBACK_URL,
        "response_type": "code",
        "scope": "https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile",
        "access_type": "offline",
    }
    auth_url = f"{GOOGLE_AUTH_URL}?{'&'.join([f'{key}={value}' for key, value in params.items()])}"
    return RedirectResponse(auth_url)

@router.get("/callback")
async def callback(code: str):
    try:
        # Tukar code dengan token
        async with httpx.AsyncClient() as client:
            token_response = await client.post(
                GOOGLE_TOKEN_URL,
                data={
                    "client_id": settings.GOOGLE_CLIENT_ID,
                    "client_secret": settings.GOOGLE_CLIENT_SECRET,
                    "redirect_uri": settings.CALLBACK_URL,
                    "grant_type": "authorization_code",
                    "code": code,
                },
            )
        token_response.raise_for_status()
        tokens = token_response.json()

        # Dapatkan informasi pengguna
        async with httpx.AsyncClient() as client:
            userinfo_response = await client.get(
                GOOGLE_USERINFO_URL,
                headers={"Authorization": f"Bearer {tokens['access_token']}"},
            )
        userinfo_response.raise_for_status()
        user_info = userinfo_response.json()

        # Ekstrak data pengguna
        user_email = user_info.get("email")
        user_name = user_info.get("name")
        if not user_email or not user_name:
            raise HTTPException(status_code=400, detail="Email atau nama tidak ditemukan dari Google.")

        # Periksa apakah pengguna sudah ada di database
        existing_user = supabase.table("users").select("*").eq("email", user_email).execute()
        if not existing_user.data:
            # Jika pengguna baru, tambahkan ke database
            supabase.table("users").insert({
                "email": user_email,
                "name": user_name,
                "preferences": None  # Atau set nilai default
            }).execute()

        # Redirect ke homepage
        return RedirectResponse("/home")

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error during OAuth callback: {str(e)}")

# Tambahkan endpoint ini di auth.py

@router.get("/me")
async def get_current_user(request: Request):
    try:
        # Ambil token dari header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        
        token = auth_header.split(" ")[1]
        
        # Verifikasi token dan dapatkan user data dari Supabase
        user = supabase.auth.get_user(token)
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
            
        return user.data
        
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid authentication token")