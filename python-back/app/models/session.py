"""
会话模型
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from app.db.database import Base


class Session(Base):
    """会话模型"""
    
    __tablename__ = "sessions"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    session_id = Column(String(50), unique=True, index=True, nullable=False, comment="会话唯一标识")
    title = Column(String(200), nullable=False, default="新对话", comment="会话标题")
    summary = Column(Text, nullable=True, comment="会话摘要")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False, comment="更新时间")
    
    # 关系
    messages = relationship("Message", back_populates="session", cascade="all, delete-orphan")
    files = relationship("File", back_populates="session", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Session(id={self.id}, session_id={self.session_id}, title={self.title})>"

