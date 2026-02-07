from fastapi import APIRouter
from app.api.v1.endpoints import skills, categories, projects, auth, wallet

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["认证"])
api_router.include_router(skills.router, prefix="/skills", tags=["Skill管理"])
api_router.include_router(categories.router, prefix="/categories", tags=["分类管理"])
api_router.include_router(projects.router, prefix="/projects", tags=["项目管理"])
api_router.include_router(wallet.router, prefix="/user", tags=["钱包和使用记录"])
