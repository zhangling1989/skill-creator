from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db

router = APIRouter()

@router.post("/login")
def login():
    """SSO 登录"""
    return {"message": "SSO 登录接口"}

@router.post("/logout")
def logout():
    """登出"""
    return {"message": "登出接口"}

@router.get("/me")
def get_current_user():
    """获取当前用户信息"""
    return {"message": "获取用户信息接口"}

@router.get("/callback")
def auth_callback():
    """SSO 回调"""
    return {"message": "SSO 回调接口"}
