from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.core.database import get_db
from app.models.telegram_bot import TelegramBot
from app.models.user import User
from app.schemas.telegram_bot import TelegramBotCreate, TelegramBotUpdate, TelegramBotResponse
from app.api.deps import get_current_user
from aiogram import Bot
from aiogram.exceptions import TelegramUnauthorizedError

router = APIRouter(prefix="/bots", tags=["bots"])

@router.get("/", response_model=List[TelegramBotResponse])
async def get_user_bots(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Получить список ботов текущего пользователя"""
    result = await db.execute(
        select(TelegramBot).where(TelegramBot.user_id == current_user.id)
    )
    bots = result.scalars().all()
    return bots

@router.post("/", response_model=TelegramBotResponse)
async def create_bot(
    bot_data: TelegramBotCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Добавить нового бота"""
    # Проверяем токен через Telegram API
    try:
        bot = Bot(token=bot_data.bot_token)
        bot_info = await bot.get_me()
        await bot.session.close()
    except TelegramUnauthorizedError:
        raise HTTPException(
            status_code=400, 
            detail="Invalid bot token"
        )
    except Exception as e:
        raise HTTPException(
            status_code=400, 
            detail=f"Error validating bot: {str(e)}"
        )
    
    # Проверяем, не добавлен ли уже этот бот
    existing = await db.execute(
        select(TelegramBot).where(TelegramBot.bot_token == bot_data.bot_token)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=400, 
            detail="Bot already registered"
        )
    
    # Создаём запись в БД
    telegram_bot = TelegramBot(
        user_id=current_user.id,
        bot_token=bot_data.bot_token,
        bot_username=bot_info.username,
        bot_name=bot_data.bot_name or bot_info.full_name
    )
    
    db.add(telegram_bot)
    await db.commit()
    await db.refresh(telegram_bot)
    
    return telegram_bot

@router.get("/{bot_id}", response_model=TelegramBotResponse)
async def get_bot(
    bot_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Получить информацию о боте"""
    result = await db.execute(
        select(TelegramBot).where(
            TelegramBot.id == bot_id,
            TelegramBot.user_id == current_user.id
        )
    )
    bot = result.scalar_one_or_none()
    
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")
    
    return bot

@router.put("/{bot_id}", response_model=TelegramBotResponse)
async def update_bot(
    bot_id: int,
    bot_update: TelegramBotUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Обновить информацию о боте"""
    result = await db.execute(
        select(TelegramBot).where(
            TelegramBot.id == bot_id,
            TelegramBot.user_id == current_user.id
        )
    )
    bot = result.scalar_one_or_none()
    
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")
    
    # Обновляем поля
    if bot_update.bot_name is not None:
        bot.bot_name = bot_update.bot_name
    if bot_update.is_active is not None:
        bot.is_active = bot_update.is_active
    
    await db.commit()
    await db.refresh(bot)
    
    return bot

@router.delete("/{bot_id}")
async def delete_bot(
    bot_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Удалить бота"""
    result = await db.execute(
        select(TelegramBot).where(
            TelegramBot.id == bot_id,
            TelegramBot.user_id == current_user.id
        )
    )
    bot = result.scalar_one_or_none()
    
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")
    
    await db.delete(bot)
    await db.commit()
    
    return {"message": "Bot deleted successfully"}
