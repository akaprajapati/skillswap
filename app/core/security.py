from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
import os
from dotenv import load_dotenv
import hashlib

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

if not SECRET_KEY:
    raise ValueError("SECRET_KEY not set in environment")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    hashed = hashlib.sha256(password.encode()).hexdigest()
    return pwd_context.hash(hashed)


def verify_password(plain, hashed):
    try:
        plain_hash = hashlib.sha256(plain.encode()).hexdigest()
        return pwd_context.verify(plain_hash, hashed)
    except Exception:
        return False


def create_access_token(data: dict, expires_delta: int = 60):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)