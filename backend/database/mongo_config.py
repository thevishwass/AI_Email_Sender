from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_URI)

db = client["AI_Email_Sender"]          # Database
users_collection = db["users"]          # Users collection
cover_letters_collection = db["cover"]  # Cover letters collection
security_settings_collection = db["security_settings"]
