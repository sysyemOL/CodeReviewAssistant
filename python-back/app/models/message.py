"""
消息模型
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from enum import Enum
from app.db.database import Base


class MessageRole(str, Enum):
    """消息角色枚举"""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class Message(Base):
    """消息模型"""
    
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    message_id = Column(String(50), unique=True, index=True, nullable=False, comment="消息唯一标识")
    session_id = Column(String(50), ForeignKey("sessions.session_id"), nullable=False, comment="所属会话ID")
    role = Column(SQLEnum(MessageRole), nullable=False, comment="消息角色")
    content = Column(Text, nullable=False, comment="消息内容")
    thinking_process = Column(Text, nullable=True, comment="AI思考过程")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, comment="创建时间")
    
    # 关系
    session = relationship("Session", back_populates="messages")
    
    def __repr__(self):
        return f"<Message(id={self.id}, role={self.role}, session_id={self.session_id})>"

