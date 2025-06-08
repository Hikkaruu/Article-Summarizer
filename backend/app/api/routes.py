from fastapi import APIRouter, HTTPException
from app.models.link import LinkIn, LinkOut
from app.services.db import collection
from app.tasks.summarize import summarize_url
from bson import ObjectId
from bson.errors import InvalidId
from datetime import datetime, timezone
import logging

router = APIRouter()

@router.post("/submit", response_model=LinkOut)
async def submit_link(link: LinkIn):
    now = datetime.now(timezone.utc)
    doc = {
        "url": str(link.url),
        "summary": None,
        "status": "pending",
        "created_at": now,
        "updated_at": now,
        "finished_at": None,
        "language": link.language
    }
    result = await collection.insert_one(doc)
    link_id = str(result.inserted_id)

    summarize_url.delay(link_id, str(link.url), str(link.language))

    return {
        "id": link_id,
        "url": link.url,
        "summary": None,
        "status": "pending",
        "progress": doc.get("progress", 0),
        "created_at": now,
        "updated_at": now,
        "finished_at": None,
        "language": link.language
    }

@router.get("/result/{link_id}", response_model=LinkOut)
async def get_result(link_id: str):
    try:
        oid = ObjectId(link_id)
    except InvalidId:
        raise HTTPException(status_code=404, detail="Link not found")

    doc = await collection.find_one({"_id": oid})
    if not doc:
        raise HTTPException(status_code=404, detail="Link not found")

    return {
        "id": str(doc["_id"]),
        "url": doc["url"],
        "summary": doc.get("summary"),
        "status": doc["status"],
        "progress": doc.get("progress", 0),
        "created_at": doc.get("created_at"),
        "updated_at": doc.get("updated_at"),
        "finished_at": doc.get("finished_at"),
        "language": doc.get("language", "English")
    }
