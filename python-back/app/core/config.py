"""
配置管理模块
"""
from typing import List, Optional, Any
from pydantic_settings import BaseSettings
from pydantic import field_validator
import json
import os


class Settings(BaseSettings):
    """应用配置"""
    
    # API配置
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "AI Code Review Assistant"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # 服务器配置
    HOST: str = "localhost"  # 使用localhost避免CORS问题
    PORT: int = 8000
    
    # 数据库配置
    DATABASE_URL: str = "sqlite:///./app.db"
    
    # OpenAI配置（Day 3集成AI时配置）
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL: str = "gpt-4o-mini"
    OPENAI_TEMPERATURE: float = 0.2
    OPENAI_MAX_TOKENS: int = 8000
    
    # CORS配置
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",  # Edge浏览器可能使用127.0.0.1
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ]
    
    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: Any) -> List[str]:
        """解析CORS origins"""
        if isinstance(v, str):
            return json.loads(v)
        return v
    
    # 文件上传配置
    MAX_UPLOAD_SIZE: int = 10485760  # 10MB
    UPLOAD_DIR: str = "./uploads"
    ALLOWED_EXTENSIONS: List[str] = [".py", ".js", ".jsx", ".ts", ".tsx", ".java", ".go", ".cpp", ".c", ".h", ".hpp"]
    
    @field_validator("ALLOWED_EXTENSIONS", mode="before")
    @classmethod
    def parse_allowed_extensions(cls, v: Any) -> List[str]:
        """解析允许的文件扩展名"""
        if isinstance(v, str):
            return json.loads(v)
        return v
    
    # 会话配置
    SESSION_EXPIRE_MINUTES: int = 60
    MAX_SESSIONS_PER_USER: int = 100
    
    # 日志配置
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "./logs/app.log"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# 创建全局配置实例
settings = Settings()

