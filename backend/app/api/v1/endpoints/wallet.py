from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.schemas.skill import (
    WalletResponse, TransactionResponse, TransactionListResponse,
    SkillUsageCreate, SkillUsageResponse, SkillResponse
)
from app.models.skill import UserWallet, WalletTransaction, SkillUsageLog
from app.services.wallet_service import wallet_service
from typing import List

router = APIRouter()

def get_current_user_open_id():
    """获取当前用户的 open_id (需要实现 SSO 认证)"""
    # TODO: 从 JWT token 或 session 中获取
    return "test_open_id"

@router.get("/wallet", response_model=WalletResponse)
def get_wallet(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user_open_id)
):
    """获取用户钱包信息"""
    wallet = wallet_service.get_or_create_wallet(db, current_user)
    return wallet

@router.post("/wallet/recharge")
def recharge_wallet(
    amount: float,
    description: str = None,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user_open_id)
):
    """充值"""
    result = wallet_service.recharge(db, current_user, amount, description)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return result

@router.get("/wallet/transactions", response_model=TransactionListResponse)
def list_transactions(
    page: int = 1,
    page_size: int = 20,
    transaction_type: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user_open_id)
):
    """获取交易记录"""
    query = db.query(WalletTransaction).filter(
        WalletTransaction.user_open_id == current_user
    )
    
    if transaction_type:
        query = query.filter(WalletTransaction.transaction_type == transaction_type)
    
    total = query.count()
    items = query.order_by(
        WalletTransaction.created_at.desc()
    ).offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": items
    }

@router.post("/skills/use", response_model=dict)
def use_skill(
    usage: SkillUsageCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user_open_id)
):
    """使用 Skill（由 Agent 调用）
    
    这个接口会：
    1. 检查用户是否收藏了该 Skill
    2. 根据 Skill 定价扣费
    3. 记录使用日志
    4. 给 Skill 作者增加收入
    """
    result = wallet_service.charge_for_skill_usage(
        db=db,
        skill_id=usage.skill_id,
        user_open_id=current_user,
        agent_id=usage.agent_id,
        usage_type=usage.usage_type,
        request_data=usage.request_data
    )
    
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    
    return result

@router.get("/skills/usage-logs", response_model=List[SkillUsageResponse])
def list_usage_logs(
    page: int = 1,
    page_size: int = 20,
    skill_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user_open_id)
):
    """获取 Skill 使用记录"""
    query = db.query(SkillUsageLog).filter(
        SkillUsageLog.user_open_id == current_user
    )
    
    if skill_id:
        query = query.filter(SkillUsageLog.skill_id == skill_id)
    
    logs = query.order_by(
        SkillUsageLog.created_at.desc()
    ).offset((page - 1) * page_size).limit(page_size).all()
    
    return logs

@router.get("/skills/starred", response_model=List[SkillResponse])
def list_starred_skills(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user_open_id)
):
    """获取我的收藏（用户收藏的所有 Skill）"""
    skills = wallet_service.get_user_starred_skills(db, current_user)
    return skills

@router.get("/skills/income-stats")
def get_income_stats(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user_open_id)
):
    """获取我的 Skill 收入统计"""
    from app.models.skill import Skill
    from sqlalchemy import func
    
    # 获取我的所有 Skill
    my_skills = db.query(Skill).filter(
        Skill.owner_open_id == current_user,
        Skill.status == 1
    ).all()
    
    # 统计每个 Skill 的使用次数和收入
    skill_stats = []
    for skill in my_skills:
        usage_count = db.query(func.count(SkillUsageLog.id)).filter(
            SkillUsageLog.skill_id == skill.id,
            SkillUsageLog.status == 1
        ).scalar()
        
        total_income = db.query(func.sum(SkillUsageLog.charge_amount)).filter(
            SkillUsageLog.skill_id == skill.id,
            SkillUsageLog.status == 1
        ).scalar() or 0
        
        skill_stats.append({
            "skill_id": skill.id,
            "skill_name": skill.skill_name,
            "price": float(skill.price),
            "pricing_model": skill.pricing_model,
            "usage_count": usage_count,
            "total_income": float(total_income)
        })
    
    # 总收入
    wallet = wallet_service.get_or_create_wallet(db, current_user)
    
    return {
        "total_income": float(wallet.total_income),
        "current_balance": float(wallet.balance),
        "skills": skill_stats
    }
