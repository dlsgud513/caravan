import os
import httpx
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, Optional

from jose import JWTError, jwt
from dotenv import load_dotenv
from passlib.context import CryptContext

from src.models.user import User
from src.repositories.user_repository import UserRepository

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Load environment variables from .env file
load_dotenv()

class AuthService:
    """
    Handles all authentication-related logic, including JWT, OAuth2, and direct auth.
    """
    # JWT settings
    SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

    # Google OAuth2 settings
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
    GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
    GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
    GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    # --- Password Hashing ---
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        print(f"--- DEBUG: About to hash password. Value: '{password}', Type: {type(password)} ---")
        return pwd_context.hash(password)

    # --- Token Creation ---
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Creates a new JWT access token."""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

    # --- Direct Authentication ---
    def register_user(self, name: str, email: str, password: str) -> User:
        """Registers a new user with email and password."""
        if self.user_repository.find_by_email(email):
            raise ValueError("User with this email already exists")
        
        hashed_password = self.get_password_hash(password)
        new_user = User(
            name=name,
            email=email,
            hashed_password=hashed_password,
            provider="direct"
        )
        return self.user_repository.save(new_user)

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticates a user by email and password."""
        user = self.user_repository.find_by_email(email)
        if not user or not user.hashed_password:
            return None
        if not self.verify_password(password, user.hashed_password):
            return None
        return user

    # --- Google OAuth2 ---
    async def _get_google_token(self, code: str) -> Dict[str, Any]:
        """Exchange authorization code for Google access token."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.GOOGLE_TOKEN_URL,
                data={
                    "code": code,
                    "client_id": self.GOOGLE_CLIENT_ID,
                    "client_secret": self.GOOGLE_CLIENT_SECRET,
                    "redirect_uri": self.GOOGLE_REDIRECT_URI,
                    "grant_type": "authorization_code",
                },
            )
            response.raise_for_status()
            return response.json()

    async def _get_google_user_info(self, token: str) -> Dict[str, Any]:
        """Fetch user information from Google using access token."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                self.GOOGLE_USERINFO_URL,
                headers={"Authorization": f"Bearer {token}"},
            )
            response.raise_for_status()
            return response.json()

    async def handle_google_login(self, code: str) -> str:
        """Main logic for Google login."""
        google_token_data = await self._get_google_token(code)
        access_token = google_token_data["access_token"]
        user_info = await self._get_google_user_info(access_token)

        user = self.user_repository.find_by_email(user_info["email"])
        if not user:
            new_user = User(
                email=user_info["email"],
                name=user_info.get("name", "New User"),
                picture=user_info.get("picture"),
                provider="google",
                social_id=user_info["sub"],
            )
            user = self.user_repository.save(new_user)

        access_token_expires = timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        app_jwt = self.create_access_token(
            data={"sub": user.email, "user_id": user.user_id},
            expires_delta=access_token_expires,
        )
        return app_jwt

    def get_google_auth_url(self) -> str:
        """Constructs the Google authorization URL for the frontend."""
        return (
            f"https://accounts.google.com/o/oauth2/v2/auth?"
            f"client_id={self.GOOGLE_CLIENT_ID}&"
            f"redirect_uri={self.GOOGLE_REDIRECT_URI}&"
            f"response_type=code&"
            f"scope=openid%20profile%20email"
        )