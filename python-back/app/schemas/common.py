"""
通用响应模型
"""
from typing import Optional, Any, Generic, TypeVar
from pydantic import BaseModel

T = TypeVar('T')


class ResponseModel(BaseModel, Generic[T]):
    """统一响应模型"""
    code: int = 200
    message: str = "success"
    data: Optional[T] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "code": 200,
                "message": "success",
                "data": {}
            }
        }

