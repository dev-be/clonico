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
