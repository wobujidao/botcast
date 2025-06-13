from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Dict, Any
import logging

from app.core.database import get_db
from app.services.telegram import TelegramService
from app.models.telegram_bot import TelegramBot
from app.models.subscriber import Subscriber
from app.schemas.subscriber import SubscriberCreate

router = APIRouter(prefix="/telegram", tags=["webhook"])
logger = logging.getLogger(__name__)

@router.post("/webhook/{bot_token}")
async def telegram_webhook(
    bot_token: str,
    update: Dict[str, Any],
    db: AsyncSession = Depends(get_db)
):
    """Handle Telegram webhook updates"""
    try:
        # Находим бота по токену
        bot_result = await db.execute(
            select(TelegramBot).where(TelegramBot.bot_token == bot_token)
        )
        bot = bot_result.scalar_one_or_none()
        
        if not bot:
            raise HTTPException(status_code=404, detail="Bot not found")
        
        # Обработка сообщений
        if "message" in update:
            message = update["message"]
            
            # Обработка команды /start
            if "text" in message and message["text"].startswith("/start"):
                chat = message["chat"]
                from_user = message.get("from", {})
                
                # Проверяем, существует ли подписчик
                existing_result = await db.execute(
                    select(Subscriber).where(
                        Subscriber.bot_id == bot.id,
                        Subscriber.telegram_user_id == chat["id"]
                    )
                )
                existing = existing_result.scalar_one_or_none()
                
                if existing:
                    # Обновляем информацию
                    existing.username = from_user.get("username")
                    existing.first_name = from_user.get("first_name")
                    existing.last_name = from_user.get("last_name")
                    existing.is_active = True
                    existing.is_blocked = False
                    await db.commit()
                    response_text = "🎉 С возвращением! Вы уже подписаны на рассылки."
                else:
                    # Создаем нового подписчика
                    subscriber = Subscriber(
                        bot_id=bot.id,
                        telegram_user_id=chat["id"],
                        username=from_user.get("username"),
                        first_name=from_user.get("first_name"),
                        last_name=from_user.get("last_name"),
                        language_code=from_user.get("language_code"),
                        is_active=True
                    )
                    db.add(subscriber)
                    await db.commit()
                    response_text = "🎉 Добро пожаловать! Вы успешно подписались на рассылки."
                
                # Отправляем ответ
                telegram_service = TelegramService(bot_token)
                try:
                    await telegram_service.send_message(
                        chat_id=chat["id"],
                        text=response_text
                    )
                finally:
                    await telegram_service.close()
                
                logger.info(f"Subscriber {chat['id']} processed for bot {bot.id}")
        
        return {"ok": True}
        
    except Exception as e:
        logger.error(f"Webhook error: {str(e)}")
        return {"ok": False, "error": str(e)}
