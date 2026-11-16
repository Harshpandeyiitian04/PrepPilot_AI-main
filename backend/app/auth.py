# This file handles passwords and the login pass a person carries after they sign in.

import os
import jwt
import bcrypt
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

# Reads secret settings, like the signing key, from the hidden settings file.
load_dotenv()

# The secret key used to sign login passes. A stand-in key is used if none is set.
SECRET_KEY = os.getenv("JWT_SECRET", "dev-secret-change-this-in-production")
# The kind of lock used on the login pass.
ALGORITHM = "HS256"
# How many days a login pass stays good before the person must log in again.
ACCESS_TOKEN_EXPIRE_DAYS = 7

# Scrambles a password so the real password is not saved in plain text.
def hash_password(password: str) -> str:
    # Only the first 72 characters are used, because that is all this lock can read.
    pw_bytes = password.encode("utf-8")[:72]
    hashed = bcrypt.hashpw(pw_bytes, bcrypt.gensalt())
    return hashed.decode("utf-8")

# Checks whether the password someone typed matches the scrambled one we saved.
def verify_password(plain_password: str, hashed_password: str) -> bool:
    pw_bytes = plain_password.encode("utf-8")[:72]
    return bcrypt.checkpw(pw_bytes, hashed_password.encode("utf-8"))

# Builds a login pass that says who the person is and when the pass expires.
def create_access_token(user_id: int, email: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    payload = {"sub": str(user_id), "email": email, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

# Reads a login pass and checks that it is real and not expired.
def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")
