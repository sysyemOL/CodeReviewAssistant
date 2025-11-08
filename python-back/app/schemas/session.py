"""
会话相关的Pydantic模型
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class SessionBase(BaseModel):
    """会话基础模型"""
    title: str = Field(..., max_length=200, description="会话标题")


class SessionCreate(SessionBase):
    """创建会话模型"""
    pass


class SessionUpdate(BaseModel):
    """更新会话模型"""
    title: Optional[str] = Field(None, max_length=200, description="会话标题")
    summary: Optional[str] = Field(None, description="会话摘要")


class SessionResponse(SessionBase):
    """会话响应模型"""
    session_id: str
    summary: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    message_count: int = 0
    file_count: int = 0
    
    class Config:
        from_attributes = True


class SessionList(BaseModel):
    """会话列表模型"""
    total: int
    items: List[SessionResponse]

