import asyncio
from datetime import datetime
from typing import Optional
from aiogram import Bot
from aiogram.exceptions import TelegramRetryAfter, TelegramBadRequest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import async_session_maker
from app.models.broadcast import Broadcast, BroadcastStatus
from app.models.broadcast_message import BroadcastMessage
from app.models.subscriber import Subscriber
from app.models.telegram_bot import TelegramBot
import logging

logger = logging.getLogger(__name__)

async def send_broadcast(ctx, broadcast_id: int):
    """Отправить рассылку"""
    async with async_session_maker() as db:
        # Получаем рассылку
        result = await db.execute(
            select(Broadcast).where(Broadcast.id == broadcast_id)
        )
        broadcast = result.scalar_one_or_none()
        
        if not broadcast:
            logger.error(f"Broadcast {broadcast_id} not found")
            return
        
        if broadcast.status == BroadcastStatus.CANCELLED:
            logger.info(f"Broadcast {broadcast_id} was cancelled")
            return
        
        # Обновляем статус
        broadcast.status = BroadcastStatus.IN_PROGRESS
        broadcast.started_at = datetime.utcnow()
        await db.commit()
        
        # Получаем бота
        bot_result = await db.execute(
            select(TelegramBot).where(TelegramBot.id == broadcast.bot_id)
        )
        telegram_bot = bot_result.scalar_one()
        
        # Создаем экземпляр бота
        bot = Bot(token=telegram_bot.bot_token)
        
        try:
            # Получаем активных подписчиков
            subscribers_result = await db.execute(
                select(Subscriber).where(
                    Subscriber.bot_id == broadcast.bot_id,
                    Subscriber.is_active == True,
                    Subscriber.is_blocked == False
                )
            )
            subscribers = subscribers_result.scalars().all()
            
            # Создаем записи для отправки
            for subscriber in subscribers:
                msg = BroadcastMessage(
                    broadcast_id=broadcast_id,
                    subscriber_id=subscriber.id
                )
                db.add(msg)
            await db.commit()
            
            # Отправляем сообщения
            sent_count = 0
            failed_count = 0
            
            for subscriber in subscribers:
                # Проверяем, не отменена ли рассылка
                await db.refresh(broadcast)
                if broadcast.status == BroadcastStatus.CANCELLED:
                    logger.info(f"Broadcast {broadcast_id} was cancelled during execution")
                    break
                
                try:
                    # Отправляем сообщение
                    message = await bot.send_message(
                        chat_id=subscriber.telegram_user_id,
                        text=broadcast.message_text
                    )
                    
                    # Обновляем статус сообщения
                    msg_result = await db.execute(
                        select(BroadcastMessage).where(
                            BroadcastMessage.broadcast_id == broadcast_id,
                            BroadcastMessage.subscriber_id == subscriber.id
                        )
                    )
                    msg = msg_result.scalar_one()
                    msg.is_sent = True
                    msg.message_id = message.message_id
                    msg.sent_at = datetime.utcnow()
                    
                    sent_count += 1
                    
                except TelegramBadRequest as e:
                    if "bot was blocked by the user" in str(e):
                        # Помечаем подписчика как заблокированного
                        subscriber.is_blocked = True
                    
                    # Обновляем статус сообщения
                    msg_result = await db.execute(
                        select(BroadcastMessage).where(
                            BroadcastMessage.broadcast_id == broadcast_id,
                            BroadcastMessage.subscriber_id == subscriber.id
                        )
                    )
                    msg = msg_result.scalar_one()
                    msg.is_failed = True
                    msg.error_message = str(e)
                    
                    failed_count += 1
                    logger.error(f"Failed to send message to {subscriber.telegram_user_id}: {e}")
                    
                except TelegramRetryAfter as e:
                    # Ждем указанное время
                    await asyncio.sleep(e.retry_after)
                    # Повторяем попытку
                    continue
                    
                except Exception as e:
                    failed_count += 1
                    logger.error(f"Unexpected error sending to {subscriber.telegram_user_id}: {e}")
                
                # Обновляем счетчики
                broadcast.sent_count = sent_count
                broadcast.failed_count = failed_count
                await db.commit()
                
                # Небольшая задержка между сообщениями
                await asyncio.sleep(0.05)
            
            # Завершаем рассылку
            broadcast.status = BroadcastStatus.COMPLETED
            broadcast.completed_at = datetime.utcnow()
            await db.commit()
            
            logger.info(f"Broadcast {broadcast_id} completed. Sent: {sent_count}, Failed: {failed_count}")
            
        except Exception as e:
            broadcast.status = BroadcastStatus.FAILED
            await db.commit()
            logger.error(f"Broadcast {broadcast_id} failed: {e}")
            raise
            
        finally:
            await bot.session.close()

async def process_broadcast_message(ctx, message_id: int):
    """Обработать отдельное сообщение рассылки"""
    # TODO: Реализовать для повторной отправки неудачных сообщений
    pass
