import logging
from typing import Optional
from aiogram import Bot
from aiogram.enums import ParseMode
logger = logging.getLogger(__name__)

class TelegramService:
    def __init__(self, bot_token: str):
        self.bot = Bot(token=bot_token)
    
    async def send_message(
        self, 
        chat_id: int, 
        text: str,
        parse_mode: Optional[str] = ParseMode.HTML
    ) -> bool:
        """Send message to Telegram user"""
        try:
            await self.bot.send_message(
                chat_id=chat_id,
                text=text,
                parse_mode=parse_mode
            )
            return True
        except Exception as e:
            logger.error(f"Error sending message to {chat_id}: {e}")
            return False
    
    async def close(self):
        """Close bot session"""
        await self.bot.session.close()
