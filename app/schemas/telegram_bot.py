from pydantic import BaseModel, computed_field
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
    
    @computed_field
    @property
    def is_running(self) -> bool:
        return self.is_active
    
    @computed_field
    @property 
    def name(self) -> str:
        return self.bot_name or self.bot_username or f"Bot {self.id}"
    
    @computed_field
    @property
    def description(self) -> str:
        return f"@{self.bot_username}" if self.bot_username else f"Bot ID: {self.id}"
    
    class Config:
        from_attributes = True
