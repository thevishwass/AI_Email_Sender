from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class SecuritySettingsModel(BaseModel):
    sender_email: Optional[EmailStr] = None
    passkey: Optional[str] = None
    smtp_host: Optional[str] = 'smtp.gmail.com'
    smtp_port: Optional[int] = 587
