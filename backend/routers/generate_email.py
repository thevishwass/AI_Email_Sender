import json
from fastapi import APIRouter
from schemas.email_schema import EmailRequest
from ai.gemini_email import generate_email_and_subject

router = APIRouter(prefix="/email", tags=["Email"])

@router.post("/generate")
def generate_email(req: EmailRequest):
    raw_response = generate_email_and_subject(
        req.email,
        req.jd,
    )

    # Strip backticks and parse JSON
    cleaned = raw_response.strip("` \n")  # removes ```json and ``` if present
    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError:
        data = {"subject": "", "body": cleaned}  # fallback

    # print('data', data)

    return data
