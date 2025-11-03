from fastapi import APIRouter
from pydantic import BaseModel
from ai.gemini_email import generate_email_and_subject
import json

router = APIRouter(prefix="/email", tags=["Email"])

class EmailRequest(BaseModel):
    email: str
    jd: str

@router.post("/generate")
def generate_email(req: EmailRequest):
    result_text = generate_email_and_subject(req.email, req.jd)
    
    # Clean up the string and convert to JSON
    clean_text = result_text.replace("```json", "").replace("```", "").strip()
    try:
        result_json = json.loads(clean_text)
    except:
        result_json = {"subject": "", "body": ""}

    
    return result_json
