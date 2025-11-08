"""
健康检查API
"""
from fastapi import APIRouter
from datetime import datetime
from app.schemas.common import ResponseModel

router = APIRouter()


@router.get("/", response_model=ResponseModel)
async def health_check():
    """
    健康检查接口
    """
    return ResponseModel(
        code=200,
        message="服务运行正常",
        data={
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "service": "AI Code Review Assistant"
        }
    )


@router.get("/ping", response_model=ResponseModel)
async def ping():
    """
    简单的ping接口
    """
    return ResponseModel(
        code=200,
        message="pong",
        data={"ping": "pong"}
    )

