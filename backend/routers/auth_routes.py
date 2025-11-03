# routers/auth_routes.py
from fastapi import APIRouter, HTTPException, Depends, Response
from schemas.user_schema import UserRegister, UserLogin
from services.auth_service import create_user, authenticate_user, get_current_user, create_access_token
from database.mongo_config import db
from typing import Optional
from pydantic import BaseModel
from datetime import timedelta

router = APIRouter()  # single router instance
users_collection = db["users"]

# ---------------- Register ----------------
@router.post("/auth/register")
async def register(user: UserRegister):
    # Check if user already exists
    if await users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="User already exists")

    # Pass optional cover (empty by default)
    new_user = await create_user(user)
    return {"message": "User registered successfully", "user": new_user}


# ---------------- Login ----------------
@router.post("/auth/login")
async def login(user: UserLogin, response: Response):
    auth_user = await authenticate_user(user)
    if not auth_user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token = create_access_token({"sub": auth_user["email"]})
    # Set cookie for frontend access
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,  # Change to True in production with HTTPS
        samesite="Lax"
    )
    return {"access_token": access_token, "token_type": "bearer", "user": auth_user}


# ---------------- Logout ----------------
@router.post("/auth/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Logged out successfully"}


# ---------------- User Settings ----------------
class UserSettingsUpdate(BaseModel):
    phone: str = ""
    linkedin_profile: str = ""
    portfolio_url: str = ""
    location: str = ""


@router.get("/user/settings")
async def get_user_settings(current_user: dict = Depends(get_current_user)):
    user_email = current_user["email"]
    user = await users_collection.find_one({"email": user_email}, {"_id": 0, "password": 0})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "phone": user.get("phone", ""),
        "linkedin_profile": user.get("linkedin_profile", ""),
        "portfolio_url": user.get("portfolio_url", ""),
        "location": user.get("location", "")
    }


@router.put("/user/settings")
async def update_user_settings(
    data: UserSettingsUpdate,
    current_user: dict = Depends(get_current_user)
):
    user_email = current_user["email"]
    result = await users_collection.update_one(
        {"email": user_email},
        {"$set": {
            "phone": data.phone,
            "linkedin_profile": data.linkedin_profile,
            "portfolio_url": data.portfolio_url,
            "location": data.location
        }}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "Settings updated successfully!"}
