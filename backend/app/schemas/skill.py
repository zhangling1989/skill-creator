from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class SkillBase(BaseModel):
    skill_name: str = Field(..., max_length=256)
    description: Optional[str] = None
    category_id: int
    tags: Optional[List[str]] = None
    price: float = Field(default=0.0, ge=0)
    pricing_model: str = Field(default="per_use")
    is_public: bool = True

class SkillCreate(SkillBase):
    project_id: int

class SkillUpdate(BaseModel):
    skill_name: Optional[str] = Field(None, max_length=256)
    description: Optional[str] = None
    category_id: Optional[int] = None
    tags: Optional[List[str]] = None
    price: Optional[float] = Field(None, ge=0)
    pricing_model: Optional[str] = None
    is_public: Optional[bool] = None

class SkillResponse(SkillBase):
    id: int
    slug: str
    project_id: int
    owner_open_id: str
    file_name: str
    file_size: Optional[int]
    version: str
    price: float
    pricing_model: str
    view_count: int
    download_count: int
    star_count: int
    usage_count: int
    status: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class SkillListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[SkillResponse]

class CategoryBase(BaseModel):
    category_name: str = Field(..., max_length=64)
    parent_id: int = 0
    description: Optional[str] = None
    icon: Optional[str] = None
    sort_order: int = 0

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int
    status: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class CommentCreate(BaseModel):
    content: str
    rating: Optional[int] = Field(None, ge=1, le=5)
    parent_id: int = 0

class CommentResponse(BaseModel):
    id: int
    skill_id: int
    user_open_id: str
    parent_id: int
    content: str
    rating: Optional[int]
    status: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class SkillBatchUploadResponse(BaseModel):
    skill_id: int
    total_files: int
    uploaded_files: int
    failed_files: int
    file_list: List[dict]
    message: str


# 使用记录相关
class SkillUsageCreate(BaseModel):
    skill_id: int
    agent_id: Optional[str] = None
    usage_type: str = "agent_call"
    request_data: Optional[dict] = None

class SkillUsageResponse(BaseModel):
    id: int
    skill_id: int
    user_open_id: str
    agent_id: Optional[str]
    usage_type: str
    charge_amount: float
    status: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# 钱包相关
class WalletResponse(BaseModel):
    user_open_id: str
    balance: float
    frozen_balance: float
    total_income: float
    total_expense: float
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class TransactionResponse(BaseModel):
    id: int
    transaction_no: str
    user_open_id: str
    transaction_type: str
    amount: float
    balance_before: float
    balance_after: float
    related_type: Optional[str]
    related_id: Optional[int]
    description: Optional[str]
    status: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class TransactionListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[TransactionResponse]
