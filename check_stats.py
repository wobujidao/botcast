#!/usr/bin/env python3
"""
Проверка статистики системы
"""
import asyncio
from sqlalchemy import select, func
from app.core.database import AsyncSessionLocal
from app.models.user import User
from app.models.telegram_bot import TelegramBot
from app.models.subscriber import Subscriber
from app.models.broadcast import Broadcast

async def check_stats():
    async with AsyncSessionLocal() as db:
        # Количество пользователей
        users_count = await db.scalar(select(func.count(User.id)))
        print(f"👥 Пользователей: {users_count}")
        
        # Количество ботов
        bots_count = await db.scalar(select(func.count(TelegramBot.id)))
        print(f"🤖 Ботов: {bots_count}")
        
        # Количество подписчиков
        subscribers_count = await db.scalar(select(func.count(Subscriber.id)))
        active_subscribers = await db.scalar(
            select(func.count(Subscriber.id)).where(
                Subscriber.is_active == True,
                Subscriber.is_blocked == False
            )
        )
        print(f"📊 Подписчиков: {subscribers_count} (активных: {active_subscribers})")
        
        # Количество рассылок
        broadcasts_count = await db.scalar(select(func.count(Broadcast.id)))
        print(f"📨 Рассылок: {broadcasts_count}")
        
        # Детали по ботам
        if bots_count > 0:
            print("\n📋 Детали по ботам:")
            bots = await db.execute(select(TelegramBot))
            for bot in bots.scalars():
                subs_count = await db.scalar(
                    select(func.count(Subscriber.id)).where(
                        Subscriber.bot_id == bot.id
                    )
                )
                print(f"   @{bot.bot_username}: {subs_count} подписчиков")

if __name__ == "__main__":
    asyncio.run(check_stats())
