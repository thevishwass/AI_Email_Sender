# backend/services/auth_service.py

from database.mongo_config import db
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordBearer

# ---------------- Database ----------------
users_collection = db["users"]

# ---------------- Password hashing ----------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
BCRYPT_MAX_LENGTH = 72  # max bytes for bcrypt

# ---------------- JWT Config ----------------
SECRET_KEY = "hello123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# ---------------- Create user ----------------
async def create_user(user):
    """
    Create a new user in MongoDB with password truncated to 72 bytes.
    """
    password_to_hash = str(user.password or "")[:BCRYPT_MAX_LENGTH]
    hashed_password = pwd_context.hash(password_to_hash)

    user_dict = {
        "name": user.name,
        "email": user.email,
        "password": hashed_password,
        "phone": getattr(user, "phone", ""),
        "location": getattr(user, "location", ""),
        "portfolio_url": getattr(user, "portfolio_url", ""),
        "linkedin_profile": getattr(user, "linkedin_profile", ""),
        "created_at": datetime.now(timezone.utc),
    }

    await users_collection.insert_one(user_dict)
    return {"name": user.name, "email": user.email}


# ---------------- Authenticate user ----------------
async def authenticate_user(user):
    """
    Authenticate user: check if password matches the hashed password.
    Truncate password to 72 bytes for bcrypt.
    """
    existing_user = await users_collection.find_one({"email": user.email})
    if not existing_user:
        return False

    input_password = str(user.password or "")[:BCRYPT_MAX_LENGTH]

    if not pwd_context.verify(input_password, existing_user["password"]):
        return False

    return {"name": existing_user["name"], "email": existing_user["email"]}


# ---------------- Create JWT token ----------------
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# ---------------- Get current user ----------------
async def get_current_user(request: Request):
    """
    Get the current logged-in user from cookie or Authorization header.
    """
    token = request.cookies.get("access_token")

    if not token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"email": email}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
