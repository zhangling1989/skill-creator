from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.skill import CategoryCreate, CategoryResponse
from app.models.skill import SkillCategory

router = APIRouter()

@router.get("", response_model=List[CategoryResponse])
def list_categories(db: Session = Depends(get_db)):
    """获取分类列表"""
    categories = db.query(SkillCategory).filter(
        SkillCategory.status == 1
    ).order_by(SkillCategory.sort_order).all()
    return categories

@router.post("", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    """创建分类"""
    existing = db.query(SkillCategory).filter(
        SkillCategory.category_name == category.category_name
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="分类已存在")
    
    new_category = SkillCategory(**category.dict())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    
    return new_category

@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    """获取分类详情"""
    category = db.query(SkillCategory).filter(
        SkillCategory.id == category_id,
        SkillCategory.status == 1
    ).first()
    
    if not category:
        raise HTTPException(status_code=404, detail="分类不存在")
    
    return category
