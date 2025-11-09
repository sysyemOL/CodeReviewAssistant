"""
API v1版本
"""
from fastapi import APIRouter
from app.api.v1 import health, sessions, messages, files, review, chat

api_router = APIRouter()

# 注册各个模块的路由
api_router.include_router(health.router, prefix="/health", tags=["健康检查"])
api_router.include_router(sessions.router, prefix="/sessions", tags=["会话管理"])
api_router.include_router(messages.router, prefix="/messages", tags=["消息管理"])
api_router.include_router(files.router, prefix="/files", tags=["文件管理"])
api_router.include_router(review.router, prefix="/review", tags=["代码审查"])
api_router.include_router(chat.router, prefix="/chat", tags=["对话聊天"])

