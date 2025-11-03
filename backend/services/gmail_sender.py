import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
from database.mongo_config import security_settings_collection

# =====================
# 🌍 Load Environment Variables
# =====================
load_dotenv()

# ✅ Default fallback credentials
DEFAULT_SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
DEFAULT_SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
DEFAULT_EMAIL = os.getenv("EMAIL_ADDRESS")
DEFAULT_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")


# =====================
# 📧 Email Sending Logic
# =====================
async def send_email_via_gmail(
    user_account_email: str,
    recipient_email: str,
    subject: str,
    body: str,
    html: bool = False,
    attachment: bytes = None,
    attachment_filename: str = None
):
    """
    Sends email using user-specific SMTP credentials stored in MongoDB.
    Falls back to default .env credentials only if user data not found.
    """

    # ✅ Fetch user’s saved SMTP settings
    settings = await security_settings_collection.find_one({"account_email": user_account_email})

    if settings:
        sender_email = settings.get("sender_email")
        smtp_password = settings.get("passkey")  # now directly stored as plain text
        smtp_host = settings.get("smtp_host") or DEFAULT_SMTP_HOST
        smtp_port = settings.get("smtp_port") or DEFAULT_SMTP_PORT
    else:
        # fallback (very rare)
        sender_email = DEFAULT_EMAIL
        smtp_password = DEFAULT_APP_PASSWORD
        smtp_host = DEFAULT_SMTP_HOST
        smtp_port = DEFAULT_SMTP_PORT

    if not sender_email:
        raise Exception("⚠️ Email Problem — missing sender email.")
    if not smtp_password:
        raise Exception("⚠️ Password Problem — missing app password.")

    # ✅ Build message
    msg = EmailMessage()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject

    if html:
        msg.add_alternative(body, subtype="html")
    else:
        msg.set_content(body)

    if attachment and attachment_filename:
        msg.add_attachment(
            attachment,
            maintype="application",
            subtype="pdf",
            filename=attachment_filename
        )

    # ✅ Send email
    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(sender_email, smtp_password)
            server.send_message(msg)

        print(f"✅ Email sent successfully to {recipient_email} from {sender_email}")
        return {"message": f"✅ Email sent successfully from {sender_email}!"}

    except smtplib.SMTPAuthenticationError:
        raise Exception(
            f"❌ Authentication failed for {sender_email}. "
            "Please verify your app password or enable 2FA."
        )
    except smtplib.SMTPConnectError:
        raise Exception(f"❌ Could not connect to SMTP server {smtp_host}:{smtp_port}")
    except Exception as e:
        raise Exception(f"❌ Failed to send email: {str(e)}")
