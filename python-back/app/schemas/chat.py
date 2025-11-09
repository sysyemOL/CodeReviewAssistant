"""
聊天相关的数据模型
"""
from pydantic import BaseModel, Field
from typing import Optional, List


class ChatRequest(BaseModel):
    """聊天请求"""
    session_id: str = Field(..., description="会话ID")
    message: str = Field(..., description="用户消息内容")
    file_ids: Optional[List[str]] = Field(default=None, description="关联的文件ID列表")
    
    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "session_abc123",
                "message": "请帮我审查这段代码",
                "file_ids": ["file_001", "file_002"]
            }
        }


class ChatResponse(BaseModel):
    """聊天响应"""
    user_message_id: str = Field(..., description="用户消息ID")
    ai_message_id: str = Field(..., description="AI消息ID")
    content: str = Field(..., description="AI回复内容")

