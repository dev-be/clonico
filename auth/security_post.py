from fastapi import Cookie, HTTPException, Request
from auth.cookies import serializer

def validation_post_success(request: Request):
    session_token = request.cookies.get("session_token")
    if not session_token:
        raise HTTPException(status_code=403, detail="Not authenticated")

    try:
        user_id = serializer.loads(session_token)
        return user_id
    except:
        raise HTTPException(status_code=403, detail="Invalid session")