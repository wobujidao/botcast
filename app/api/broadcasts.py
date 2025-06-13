from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional
from datetime import datetime
from app.core.database import get_db
from app.models.user import User
from app.models.telegram_bot import TelegramBot
from app.models.broadcast import Broadcast, BroadcastStatus
from app.models.subscriber import Subscriber
from app.models.broadcast_message import BroadcastMessage
from app.schemas.broadcast import BroadcastCreate, BroadcastUpdate, BroadcastResponse, BroadcastStats
from app.api.deps import get_current_user
from app.workers.broadcast import send_broadcast
#from app.workers.broadcast import send_broadcast_task

router = APIRouter(prefix="/broadcasts", tags=["broadcasts"])

@router.get("/", response_model=List[BroadcastResponse])
async def get_broadcasts(
    bot_id: Optional[int] = None,
    status: Optional[BroadcastStatus] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Получить список рассылок"""
    query = select(Broadcast).join(TelegramBot).where(
        TelegramBot.user_id == current_user.id
    )
    
    if bot_id:
        query = query.where(Broadcast.bot_id == bot_id)
    if status:
        query = query.where(Broadcast.status == status)
    
    result = await db.execute(query.order_by(Broadcast.created_at.desc()))
    broadcasts = result.scalars().all()
    return broadcasts
@router.post("/", response_model=BroadcastResponse)
async def create_broadcast(
    broadcast_data: BroadcastCreate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Создать новую рассылку"""
    # Проверяем, что бот принадлежит пользователю
    bot_result = await db.execute(
        select(TelegramBot).where(
            TelegramBot.id == broadcast_data.bot_id,
            TelegramBot.user_id == current_user.id
        )
    )
    bot = bot_result.scalar_one_or_none()
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")
    
    # Считаем подписчиков
    count_result = await db.execute(
        select(func.count(Subscriber.id)).where(
            Subscriber.bot_id == broadcast_data.bot_id,
            Subscriber.is_active == True,
            Subscriber.is_blocked == False
        )
    )
    total_recipients = count_result.scalar()
    
    # Создаём рассылку
    broadcast = Broadcast(
        bot_id=broadcast_data.bot_id,
        name=broadcast_data.name,
        message_text=broadcast_data.message_text,
        scheduled_at=broadcast_data.scheduled_at,
        total_recipients=total_recipients,
        status=BroadcastStatus.SCHEDULED if broadcast_data.scheduled_at else BroadcastStatus.DRAFT
    )
    
    db.add(broadcast)
    await db.commit()
    await db.refresh(broadcast)
    
    # Если нужно отправить сразу
    if not broadcast_data.scheduled_at:
        background_tasks.add_task(send_broadcast_task, broadcast.id)
    
    return broadcast

@router.get("/{broadcast_id}", response_model=BroadcastResponse)
async def get_broadcast(
    broadcast_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Получить информацию о рассылке"""
    result = await db.execute(
        select(Broadcast).join(TelegramBot).where(
            Broadcast.id == broadcast_id,
            TelegramBot.user_id == current_user.id
        )
    )
    broadcast = result.scalar_one_or_none()
    
    if not broadcast:
        raise HTTPException(status_code=404, detail="Broadcast not found")
    
    return broadcast

@router.post("/{broadcast_id}/start")
async def start_broadcast(
    broadcast_id: int,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Запустить рассылку"""
    result = await db.execute(
        select(Broadcast).join(TelegramBot).where(
            Broadcast.id == broadcast_id,
            TelegramBot.user_id == current_user.id
        )
    )
    broadcast = result.scalar_one_or_none()
    
    if not broadcast:
        raise HTTPException(status_code=404, detail="Broadcast not found")
    
    if broadcast.status not in [BroadcastStatus.DRAFT, BroadcastStatus.SCHEDULED]:
        raise HTTPException(status_code=400, detail="Broadcast cannot be started")
    
    # Запускаем рассылку в фоне
    background_tasks.add_task(send_broadcast_task, broadcast_id)
    
    broadcast.status = BroadcastStatus.IN_PROGRESS
    await db.commit()
    
    return {"message": "Broadcast started"}

@router.post("/{broadcast_id}/cancel")
async def cancel_broadcast(
    broadcast_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Отменить рассылку"""
    result = await db.execute(
        select(Broadcast).join(TelegramBot).where(
            Broadcast.id == broadcast_id,
            TelegramBot.user_id == current_user.id
        )
    )
    broadcast = result.scalar_one_or_none()
    
    if not broadcast:
        raise HTTPException(status_code=404, detail="Broadcast not found")
    
    if broadcast.status not in [BroadcastStatus.SCHEDULED, BroadcastStatus.IN_PROGRESS]:
        raise HTTPException(status_code=400, detail="Broadcast cannot be cancelled")
    
    broadcast.status = BroadcastStatus.CANCELLED
    await db.commit()
    
    return {"message": "Broadcast cancelled"}

@router.get("/{broadcast_id}/stats", response_model=BroadcastStats)
async def get_broadcast_stats(
    broadcast_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Получить статистику рассылки"""
    result = await db.execute(
        select(Broadcast).join(TelegramBot).where(
            Broadcast.id == broadcast_id,
            TelegramBot.user_id == current_user.id
        )
    )
    broadcast = result.scalar_one_or_none()
    
    if not broadcast:
        raise HTTPException(status_code=404, detail="Broadcast not found")
    
    success_rate = 0.0
    if broadcast.total_recipients > 0:
        success_rate = (broadcast.sent_count / broadcast.total_recipients) * 100
    
    return BroadcastStats(
        total_recipients=broadcast.total_recipients,
        sent_count=broadcast.sent_count,
        failed_count=broadcast.failed_count,
        success_rate=success_rate
    )
