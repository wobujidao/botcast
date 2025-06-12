from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey, BigInteger, String
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base

class BroadcastMessage(Base):
    __tablename__ = "broadcast_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    broadcast_id = Column(Integer, ForeignKey("broadcasts.id"), nullable=False)
    subscriber_id = Column(Integer, ForeignKey("subscribers.id"), nullable=False)
    message_id = Column(BigInteger, nullable=True)  # Telegram message ID
    is_sent = Column(Boolean, default=False)
    is_failed = Column(Boolean, default=False)
    error_message = Column(String, nullable=True)
    sent_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Отношения
    broadcast = relationship("Broadcast", back_populates="messages")
    subscriber = relationship("Subscriber")
