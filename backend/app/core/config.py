from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # 项目信息
    PROJECT_NAME: str = "Skill Hub"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # 安全配置
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24小时
    
    # 数据库配置
    DATABASE_URL: str
    
    # MinIO 配置
    MINIO_ENDPOINT: str
    MINIO_ACCESS_KEY: str
    MINIO_SECRET_KEY: str
    MINIO_SECURE: bool = False
    
    # SSO 配置
    SSO_CLIENT_ID: str
    SSO_CLIENT_SECRET: str
    SSO_AUTHORIZE_URL: str
    SSO_TOKEN_URL: str
    SSO_USERINFO_URL: str
    SSO_REDIRECT_URI: str = "http://localhost:8000/api/v1/auth/callback"
    
    # Redis 配置
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # CORS 配置
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    # 文件上传配置
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: List[str] = [".md", ".markdown", ".txt", ".py", ".js", ".ts", ".json", ".yaml", ".yml"]
    
    # 批量上传配置
    MAX_BATCH_FILES: int = 100  # 单次最多上传文件数
    MAX_BATCH_SIZE: int = 100 * 1024 * 1024  # 批量上传总大小限制 100MB
    
    # 分页配置
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
