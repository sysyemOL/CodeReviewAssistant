"""
文件相关的Pydantic模型
"""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class FileBase(BaseModel):
    """文件基础模型"""
    filename: str = Field(..., description="文件名")


class FileUpload(FileBase):
    """文件上传模型"""
    session_id: str = Field(..., description="会话ID")
    content: Optional[str] = Field(None, description="文件内容")


class FileResponse(FileBase):
    """文件响应模型"""
    file_id: str
    session_id: str
    filepath: str
    file_type: Optional[str] = None
    file_size: int
    content: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class FileList(BaseModel):
    """文件列表模型"""
    total: int
    items: List[FileResponse]

