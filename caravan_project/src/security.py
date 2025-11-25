from fastapi import Request
from typing import Optional

def get_token_from_cookie(request: Request) -> Optional[str]:
    """
    Extracts the JWT from the 'access_token' cookie.
    """
    token = request.cookies.get("access_token")
    if not token:
        return None
    
    # The token might be in the format "Bearer <token>"
    if token.startswith("Bearer "):
        return token.split("Bearer ")[1]
        
    return token
