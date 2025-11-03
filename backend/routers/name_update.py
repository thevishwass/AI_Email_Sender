from fastapi import APIRouter, Body, HTTPException, Depends
from pydantic import BaseModel
from database.mongo_config import db
from ai.gemini_email import generate_email_and_subject
import json
import re
from services.auth_service import get_current_user  # dependency

router = APIRouter(prefix="/email", tags=["Email"])
users_collection = db["users"]

async def final_data(user_email: str, company: str, recruiter_email: str, jd: str, applicant_name: str) -> dict:
    # Await the async AI function
    raw_response = await generate_email_and_subject(user_email, company, recruiter_email, jd)

    # Clean up response
    cleaned = raw_response.strip("` \n")
    if cleaned.lower().startswith("json"):
        cleaned = cleaned[4:].strip()

    match = re.search(r'\{.*\}', cleaned, re.DOTALL)
    if match:
        cleaned = match.group(0)

    try:
        data_dict = json.loads(cleaned)
    except json.JSONDecodeError:
        data_dict = {"subject": "", "body": cleaned}

    # Replace placeholder with user's name
    subject_final = data_dict.get("subject", "").replace("[name]", applicant_name)
    body_final = data_dict.get("body", "").replace("[name]", applicant_name)

    return {
        "to": recruiter_email,
        "subject": subject_final,
        "body": body_final
    }

# Pydantic schema
class FinalEmailRequest(BaseModel):
    recruiter_email: str
    jd: str
    company: str  # added company

# POST route
@router.post("/final")
async def get_final_email(
    data: FinalEmailRequest,
    current_user: dict = Depends(get_current_user)
):
    try:
        # Fetch full user from DB using email from current_user
        user_email = current_user.get("email")
        user = await users_collection.find_one({"email": user_email})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        applicant_name = user.get("name", "[name]")  # fallback just in case

        result = await final_data(
            user_email,
            data.company,
            data.recruiter_email,
            data.jd,
            applicant_name
        )
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
