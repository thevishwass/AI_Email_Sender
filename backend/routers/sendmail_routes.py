from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from pydantic import BaseModel, EmailStr
from services.gmail_sender import send_email_via_gmail
from services.auth_service import get_current_user
# from database import cover_collection
from database.mongo_config import db

cover_collection = db["cover"]

router = APIRouter(prefix="/mail", tags=["Mail"])

class SendMailRequest(BaseModel):
    to: EmailStr
    subject: str
    body: str
    html: bool = False


@router.post("/send")
async def send_mail_endpoint(
    payload: SendMailRequest,
    current_user: dict = Depends(get_current_user),
):
    user_email = current_user["email"]

    doc = await cover_collection.find_one({"user_email": user_email})
    attachment = doc.get("resume") if doc else None
    attachment_filename = doc.get("resume_filename", "resume.pdf") if doc else None

    if not payload.to or not payload.subject:
        raise HTTPException(status_code=400, detail="Missing required fields.")

    try:
        success = await send_email_via_gmail(
            user_email,
            payload.to,
            payload.subject,
            payload.body,
            payload.html,
            attachment,
            attachment_filename,
        )

        if not success:
            raise HTTPException(status_code=500, detail="Email sending failed.")

        return {"success": True, "message": "📤 Email sent successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {e}")
