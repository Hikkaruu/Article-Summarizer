from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
print(MONGO_URI)
client = AsyncIOMotorClient(MONGO_URI)
db = client["summarizer"]
collection = db["links"]