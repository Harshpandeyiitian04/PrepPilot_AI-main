# This file checks that a visitor is logged in before they can use private features.

from fastapi import Header, HTTPException
from app.auth import decode_access_token

# Reads the login pass sent with a request and returns who the person is.
def get_current_user(authorization: str = Header(...)) -> dict:
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    token = authorization.replace("Bearer ", "")
    try:
        payload = decode_access_token(token)
        return {"user_id": int(payload["sub"]), "email": payload["email"]}
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
