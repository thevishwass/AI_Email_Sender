from fastapi import APIRouter, Depends, HTTPException
from database.mongo_config import security_settings_collection
from models.security_settings import SecuritySettingsModel
from routers.auth_routes import get_current_user  # adjust path if needed

router = APIRouter(prefix="/security", tags=["Security Settings"])


# ✅ CREATE or UPDATE Security Settings
@router.post("/create-or-update")
async def create_or_update_security_settings(
    settings: SecuritySettingsModel,
    current_user: dict = Depends(get_current_user)
):
    try:
        account_email = current_user["email"]

        # Get existing settings if any
        existing_settings = await security_settings_collection.find_one(
            {"account_email": account_email}
        )

        # Build updated document
        new_settings = {
            "account_email": account_email,
            # ✅ Keep old passkey if not provided
            "passkey": settings.passkey.strip() if settings.passkey else existing_settings.get("passkey") if existing_settings else None,
            "sender_email": settings.sender_email.strip() if settings.sender_email else existing_settings.get("sender_email", ""),
            "smtp_port": settings.smtp_port or existing_settings.get("smtp_port", 587),
        }

        # Only add/update smtp_host if provided
        if settings.smtp_host and settings.smtp_host.strip():
            new_settings["smtp_host"] = settings.smtp_host.strip()
        elif existing_settings and "smtp_host" in existing_settings:
            new_settings["smtp_host"] = existing_settings["smtp_host"]

        # ✅ Upsert (create or update)
        await security_settings_collection.update_one(
            {"account_email": account_email},
            {"$set": new_settings},
            upsert=True
        )

        return {"message": "✅ Security settings saved or updated successfully!"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ✅ GET user’s saved Security Settings (without passkey)
@router.get("/me")
async def get_user_security_settings(
    current_user: dict = Depends(get_current_user)
):
    try:
        account_email = current_user["email"]

        settings = await security_settings_collection.find_one(
            {"account_email": account_email},
            {"_id": 0, "passkey": 0}  # hide passkey for safety
        )

        if not settings:
            return {"message": "⚠️ No security settings found for this account."}

        return settings

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
