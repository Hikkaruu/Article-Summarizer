from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime

class LinkIn(BaseModel):
    url: HttpUrl
    language: Optional[str] = "English"

class LinkOut(BaseModel):
    id: str
    url: HttpUrl
    summary: Optional[str] = None
    language: str
    status: str
    progress: Optional[int] = 0 
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
