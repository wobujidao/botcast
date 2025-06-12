from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TelegramBotCreate(BaseModel):
    bot_token: str
    bot_name: Optional[str] = None

class TelegramBotUpdate(BaseModel):
    bot_name: Optional[str] = None
    is_active: Optional[bool] = None

class TelegramBotResponse(BaseModel):
    id: int
    user_id: int
    bot_token: str
    bot_username: Optional[str]
    bot_name: Optional[str]
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
