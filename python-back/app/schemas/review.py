"""
代码审查相关的 Pydantic Schema
"""
from pydantic import BaseModel, Field
from typing import Optional, List


class CodeReviewRequest(BaseModel):
    """代码审查请求"""
    session_id: str = Field(..., description="会话ID")
    file_id: str = Field(..., description="文件ID")
    user_question: Optional[str] = Field(None, description="用户提出的具体问题")
    
    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "session_123",
                "file_id": "file_456",
                "user_question": "这段代码有性能问题吗？"
            }
        }


class MultiFileReviewRequest(BaseModel):
    """多文件代码审查请求"""
    session_id: str = Field(..., description="会话ID")
    file_ids: List[str] = Field(..., description="文件ID列表")
    user_question: Optional[str] = Field(None, description="用户提出的具体问题")
    
    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "session_123",
                "file_ids": ["file_456", "file_789"],
                "user_question": "这些模块之间的耦合度如何？"
            }
        }


class CodeReviewResponse(BaseModel):
    """代码审查响应"""
    session_id: str = Field(..., description="会话ID")
    review_result: str = Field(..., description="审查结果（Markdown格式）")
    message_id: str = Field(..., description="生成的消息ID")
    
    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "session_123",
                "review_result": "# 代码审查结果\n\n## 总体评分：8/10\n\n...",
                "message_id": "msg_123"
            }
        }

