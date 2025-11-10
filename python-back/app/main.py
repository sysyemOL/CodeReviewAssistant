"""
FastAPI主应用
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1 import api_router
from app.db.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    应用生命周期管理
    替代已弃用的 @app.on_event("startup") 和 @app.on_event("shutdown")
    """
    # 启动时执行
    print(f"🚀 Starting {settings.PROJECT_NAME} v{settings.VERSION}")
    print(f"📚 API文档: http://{settings.HOST}:{settings.PORT}/docs")
    
    # 初始化数据库
    try:
        init_db()
        print("✅ 数据库初始化成功")
    except Exception as e:
        print(f"❌ 数据库初始化失败: {e}")
    
    yield
    
    # 关闭时执行
    print(f"👋 Shutting down {settings.PROJECT_NAME}")


# 创建FastAPI应用
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="AI代码审查助手 - 基于LangChain和大语言模型的智能代码审查系统",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 根路由
@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "Welcome to AI Code Review Assistant API",
        "version": settings.VERSION,
        "docs": "/docs",
        "health": "/api/v1/code/health",
        "applications": {
            "code_review": "/api/v1/code/*"
        }
    }


# 注册API路由
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )

