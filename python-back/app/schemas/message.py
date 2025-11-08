"""
消息相关的Pydantic模型
"""
from datetime import datetime
from typing import List
from pydantic import BaseModel, Field
from app.models.message import MessageRole


class MessageBase(BaseModel):
    """消息基础模型"""
    content: str = Field(..., description="消息内容")


class MessageCreate(MessageBase):
    """创建消息模型"""
    role: MessageRole = Field(MessageRole.USER, description="消息角色")
    session_id: str = Field(..., description="会话ID")


class MessageResponse(MessageBase):
    """消息响应模型"""
    message_id: str
    session_id: str
    role: MessageRole
    created_at: datetime
    
    class Config:
        from_attributes = True


class MessageList(BaseModel):
    """消息列表模型"""
    total: int
    items: List[MessageResponse]

