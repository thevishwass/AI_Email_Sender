# routers/cover_routes.py
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from database.mongo_config import db
from services.auth_service import get_current_user

router = APIRouter(prefix="/cover", tags=["Cover Letter"])
cover_collection = db["cover"]

@router.put("/")
async def save_cover_letter(
    cover_text: str = Form(...),
    resume: UploadFile | None = File(None),
    current_user: dict = Depends(get_current_user)
):
    user_email = current_user["email"]

    update_data = {"cover_text": cover_text}

    if resume:
        # Read resume as bytes
        resume_bytes = await resume.read()
        update_data["resume"] = resume_bytes
        update_data["resume_filename"] = resume.filename
        update_data["has_resume"] = True

    # Upsert cover letter + optional resume
    await cover_collection.update_one(
        {"user_email": user_email},
        {"$set": update_data},
        upsert=True
    )

    return {"message": "Cover letter and resume saved successfully."}


@router.get("/")
async def get_cover_letter(current_user: dict = Depends(get_current_user)):
    user_email = current_user["email"]

    doc = await cover_collection.find_one({"user_email": user_email})
    if not doc:
        return {"cover_text": "", "has_resume": False}

    return {
        "cover_text": doc.get("cover_text", ""),
        "has_resume": "resume" in doc,
        "resume_filename": doc.get("resume_filename", ""),
    }


from fastapi.responses import StreamingResponse
import io

@router.get("/resume")
async def download_resume(current_user: dict = Depends(get_current_user)):
    user_email = current_user["email"]
    doc = await cover_collection.find_one({"user_email": user_email})

    if not doc or "resume" not in doc:
        raise HTTPException(status_code=404, detail="No resume found.")

    resume_bytes = doc["resume"]
    filename = doc.get("resume_filename", "resume.pdf")

    return StreamingResponse(
        io.BytesIO(resume_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )
