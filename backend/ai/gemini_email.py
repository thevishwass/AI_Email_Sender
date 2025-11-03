# type: ignore
import google.generativeai as genai
import os
from dotenv import load_dotenv
from database.mongo_config import db

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

cover_collection = db["cover"]

async def generate_email_and_subject(user_email: str, company: str, recruiter_email, jd):

    # Fetch cover letter from MongoDB
    user_cover = await cover_collection.find_one({"user_email": user_email})
    cover_text = user_cover["cover_text"] if user_cover else ""

    prompt = f"""
You are an expert in writing professional job application emails.

Data:
- Job Description: {jd}
- Company Name: {company} (or infer from {recruiter_email})
- Applicant's Cover Letter: {cover_text}

Return JSON only:

  "subject": "string",
  "body": "string"

Rules:
- Subject: start with "Application for", include the job title, end with "- [name]", max 8 words.
- applicant name should be [name] only nothing else.
- Body: 80 to 110 words, 2 to 3 short, readable paragraphs.
  1. Start with "Dear Hiring Team at [company name],\n\n"
     then immediately follow with "I am excited to apply for [position] at [company name]."
     Include one specific, positive line about the company (e.g., innovation, global impact, culture).
  2. Summarize the most relevant skills and achievements from the cover_text,
     clearly demonstrating how they fit the role. Use concise, confident, professional, and natural language.
  3. End with a polite, proactive call-to-action, then:
     "\nThank you for your time and consideration.\n\nSincerely,\n[name]"
- Tone: professional, confident, warm, human-like, and approachable.
- Avoid bullet points, markdown, or extra commentary.
- Keep sentences concise, natural, and recruiter-friendly; do not overcomplicate.
- Ensure the email flows smoothly, is easy to read, and feels personalized to the company and role.
"""




    response = model.generate_content(prompt)
    return response.text
