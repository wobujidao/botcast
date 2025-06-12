from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, BigInteger, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base

class Subscriber(Base):
    __tablename__ = "subscribers"
    
    id = Column(Integer, primary_key=True, index=True)
    bot_id = Column(Integer, ForeignKey("telegram_bots.id"), nullable=False)
    telegram_user_id = Column(BigInteger, nullable=False, index=True)
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    language_code = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_blocked = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Отношения
    bot = relationship("TelegramBot", back_populates="subscribers")
    
    # Уникальное ограничение
    __table_args__ = (
        UniqueConstraint('bot_id', 'telegram_user_id', name='_bot_user_uc'),
    )
