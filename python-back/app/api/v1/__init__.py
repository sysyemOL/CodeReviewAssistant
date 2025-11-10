"""
API v1版本
"""
from fastapi import APIRouter
from app.api.v1 import health, sessions, messages, files, review, chat

api_router = APIRouter()

# 为代码审查助手创建独立的路由组
# 添加 /code 前缀，为未来的其他AI应用（如文档助手、数据分析等）预留命名空间
code_router = APIRouter(prefix="/code")

# 注册各个模块的路由（代码审查相关）
code_router.include_router(health.router, prefix="/health", tags=["代码审查-健康检查"])
code_router.include_router(sessions.router, prefix="/sessions", tags=["代码审查-会话管理"])
code_router.include_router(messages.router, prefix="/messages", tags=["代码审查-消息管理"])
code_router.include_router(files.router, prefix="/files", tags=["代码审查-文件管理"])
code_router.include_router(review.router, prefix="/review", tags=["代码审查-代码审查"])
code_router.include_router(chat.router, prefix="/chat", tags=["代码审查-对话聊天"])

# 将代码审查路由组注册到主路由
api_router.include_router(code_router)

