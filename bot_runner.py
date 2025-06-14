import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.models.telegram_bot import TelegramBot
from app.models.subscriber import Subscriber

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создаем engine и session
engine = create_async_engine(settings.DATABASE_URL)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Словарь для хранения запущенных ботов
active_bots = {}

async def start_handler(message: Message, bot_id: int):
    """Обработчик команды /start"""
    async with async_session_maker() as session:
        # Проверяем, есть ли уже подписчик
        existing = await session.execute(
            select(Subscriber).where(
                Subscriber.bot_id == bot_id,
                Subscriber.telegram_user_id == message.from_user.id
            )
        )
        if not existing.scalar_one_or_none():
            # Добавляем нового подписчика
            subscriber = Subscriber(
                bot_id=bot_id,
                telegram_user_id=message.from_user.id,
                username=message.from_user.username,
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name
            )
            session.add(subscriber)
            await session.commit()
            await message.answer("✅ Добро пожаловать! Вы успешно подписались на рассылку.")
        else:
            await message.answer("ℹ️ Вы уже подписаны на рассылку.")

async def setup_bot(bot_token: str, bot_id: int):
    """Настройка и запуск бота"""
    bot = Bot(token=bot_token)
    dp = Dispatcher()
    
    # Регистрируем обработчик команды /start
    @dp.message(Command("start"))
    async def cmd_start(message: Message):
        await start_handler(message, bot_id)
    
    return bot, dp

async def run_bot(bot_token: str, bot_id: int):
    """Запуск бота"""
    try:
        bot, dp = await setup_bot(bot_token, bot_id)
        logger.info(f"Starting bot {bot_id}...")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Error running bot {bot_id}: {e}")

async def main():
    """Главная функция"""
    async with async_session_maker() as session:
        # Получаем все активные боты
        result = await session.execute(
            select(TelegramBot).where(TelegramBot.is_active == True)
        )
        bots = result.scalars().all()
        
        if not bots:
            logger.info("No active bots found")
            return
        
        # Запускаем все активные боты
        tasks = []
        for bot in bots:
            logger.info(f"Starting bot: {bot.bot_username} (ID: {bot.id})")
            task = asyncio.create_task(run_bot(bot.bot_token, bot.id))
            tasks.append(task)
            active_bots[bot.id] = task
        
        # Ждем завершения всех задач
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
