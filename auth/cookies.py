from datetime import datetime, timedelta, timezone
from fastapi import Response
from itsdangerous import URLSafeTimedSerializer

SECRET_KEY = "testandocookies"
serializer = URLSafeTimedSerializer(SECRET_KEY)

def create_token(user_id: str) -> str:
    return serializer.dumps(user_id)

def decode_token(token: str) -> str:
    try:
        user_id = serializer.loads(token, max_age=3600)
        return user_id
    
    except Exception:
        return  None

def remover_cookies(response: Response):
    response.delete_cookie(key="session_token")
    