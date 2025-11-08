"""
消息管理API（占位符，Day 2实现）
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def get_messages():
    """获取消息列表（待实现）"""
    return {"message": "消息管理API待实现"}

