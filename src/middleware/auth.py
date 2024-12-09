import json
from fastapi import Depends, HTTPException
from fastapi.security.http import HTTPAuthorizationCredentials, HTTPBase
from pydantic import BaseModel
from typing import Optional
from urllib.parse import unquote

telegram_authentication_schema = HTTPBase(scheme="twa")

class TelegramUser(BaseModel):
    id: int
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    language_code: Optional[str] = None
    is_premium: Optional[bool] = None
    allows_write_to_pm: Optional[bool] = None

def get_current_user(
    auth_cred: HTTPAuthorizationCredentials = Depends(telegram_authentication_schema),
) -> TelegramUser:
    if not auth_cred or not auth_cred.credentials:
        raise HTTPException(
            status_code=401,
            detail="Missing or invalid authorization credentials."
        )

    try:
        init_data = dict(param.split('=') for param in auth_cred.credentials.split('&'))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid init data format: {str(e)}")

    print("Init Data:", init_data)  

    user_encoded = init_data.get("user")
    if not user_encoded:
        raise HTTPException(status_code=400, detail="User data not found in init data.")
    
    user_json = unquote(user_encoded)  

    try:
        user_data = json.loads(user_json)
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=400, detail=f"Invalid user data format: {str(e)}")

    return TelegramUser(**user_data)
