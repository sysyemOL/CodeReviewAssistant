"""
统一响应格式
"""
from typing import Any, Optional


def success_response(
    data: Any = None,
    message: str = "操作成功",
    code: int = 200
) -> dict:
    """
    成功响应
    
    Args:
        data: 响应数据
        message: 响应消息
        code: 响应代码
        
    Returns:
        统一格式的响应字典
    """
    return {
        "code": code,
        "message": message,
        "data": data
    }


def error_response(
    message: str = "操作失败",
    code: int = 400,
    data: Any = None
) -> dict:
    """
    错误响应
    
    Args:
        message: 错误消息
        code: 错误代码
        data: 错误详情
        
    Returns:
        统一格式的错误响应字典
    """
    return {
        "code": code,
        "message": message,
        "data": data
    }

