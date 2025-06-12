from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from app.models.broadcast import BroadcastStatus

class BroadcastCreate(BaseModel):
    bot_id: int
    name: str
    message_text: str
    scheduled_at: Optional[datetime] = None

class BroadcastUpdate(BaseModel):
    name: Optional[str] = None
    message_text: Optional[str] = None
    scheduled_at: Optional[datetime] = None

class BroadcastResponse(BaseModel):
    id: int
    bot_id: int
    name: str
    message_text: str
    status: BroadcastStatus
    scheduled_at: Optional[datetime]
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    total_recipients: int
    sent_count: int
    failed_count: int
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class BroadcastStats(BaseModel):
    total_recipients: int
    sent_count: int
    failed_count: int
    success_rate: float
