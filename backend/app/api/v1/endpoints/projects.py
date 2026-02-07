from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db

router = APIRouter()

@router.get("")
def list_projects(db: Session = Depends(get_db)):
    """获取项目列表"""
    return {"message": "项目列表接口"}

@router.post("", status_code=status.HTTP_201_CREATED)
def create_project(db: Session = Depends(get_db)):
    """创建项目"""
    return {"message": "创建项目接口"}
