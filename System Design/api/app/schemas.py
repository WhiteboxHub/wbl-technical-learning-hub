from datetime import datetime
from pydantic import BaseModel, HttpUrl

class ShortenRequest(BaseModel):
    url: str
    custom_code: str | None = None
    async_queue: bool = False

class ShortenResponse(BaseModel):
    short_code: str
    short_url: str
    original_url: str
    created_at: datetime
    queued: bool = False

class URLStats(BaseModel):
    short_code: str
    original_url: str
    clicks: int
    created_at: datetime
    cached: bool
