from sqlalchemy import Column, BigInteger, String, Text, Integer, TIMESTAMP, ForeignKey, JSON, DECIMAL
from sqlalchemy.sql import func
from app.core.database import Base

class Skill(Base):
    __tablename__ = "skills"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    skill_name = Column(String(256), nullable=False, index=True)
    slug = Column(String(256), nullable=False, index=True)
    description = Column(Text)
    category_id = Column(BigInteger, ForeignKey("skill_categories.id"), nullable=False, index=True)
    project_id = Column(BigInteger, ForeignKey("projects.id"), nullable=False, index=True)
    owner_open_id = Column(String(128), nullable=False, index=True)
    file_path = Column(String(1024), nullable=False)
    file_name = Column(String(256), nullable=False)
    file_size = Column(BigInteger)
    file_hash = Column(String(64), index=True)
    version = Column(String(32), default="1.0.0")
    tags = Column(JSON)
    skill_metadata = Column(JSON)  # 重命名避免与 SQLAlchemy 的 metadata 冲突
    price = Column(DECIMAL(10, 2), default=0.00)
    pricing_model = Column(String(32), default="per_use")
    view_count = Column(Integer, default=0)
    download_count = Column(Integer, default=0)
    star_count = Column(Integer, default=0)
    usage_count = Column(Integer, default=0)
    is_public = Column(Integer, default=1)
    status = Column(Integer, default=1)
    created_at = Column(TIMESTAMP, server_default=func.now(), index=True)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

class SkillCategory(Base):
    __tablename__ = "skill_categories"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    category_name = Column(String(64), unique=True, nullable=False)
    parent_id = Column(BigInteger, default=0, index=True)
    description = Column(String(512))
    icon = Column(String(256))
    sort_order = Column(Integer, default=0)
    status = Column(Integer, default=1)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

class SkillVersion(Base):
    __tablename__ = "skill_versions"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    skill_id = Column(BigInteger, ForeignKey("skills.id"), nullable=False, index=True)
    version = Column(String(32), nullable=False)
    file_path = Column(String(1024), nullable=False)
    file_hash = Column(String(64))
    change_log = Column(Text)
    created_by = Column(String(128), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

class SkillStar(Base):
    __tablename__ = "skill_stars"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    skill_id = Column(BigInteger, ForeignKey("skills.id"), nullable=False, index=True)
    user_open_id = Column(String(128), nullable=False, index=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

class SkillComment(Base):
    __tablename__ = "skill_comments"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    skill_id = Column(BigInteger, ForeignKey("skills.id"), nullable=False, index=True)
    user_open_id = Column(String(128), nullable=False, index=True)
    parent_id = Column(BigInteger, default=0)
    content = Column(Text, nullable=False)
    rating = Column(Integer)
    status = Column(Integer, default=1)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())


class SkillUsageLog(Base):
    __tablename__ = "skill_usage_logs"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    skill_id = Column(BigInteger, ForeignKey("skills.id"), nullable=False, index=True)
    user_open_id = Column(String(128), nullable=False, index=True)
    agent_id = Column(String(128), index=True)
    usage_type = Column(String(32), default="agent_call")
    charge_amount = Column(DECIMAL(10, 2), default=0.00)
    status = Column(Integer, default=1)
    request_data = Column(JSON)
    response_data = Column(JSON)
    created_at = Column(TIMESTAMP, server_default=func.now(), index=True)

class UserWallet(Base):
    __tablename__ = "user_wallets"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_open_id = Column(String(128), unique=True, nullable=False, index=True)
    balance = Column(DECIMAL(10, 2), default=0.00)
    frozen_balance = Column(DECIMAL(10, 2), default=0.00)
    total_income = Column(DECIMAL(10, 2), default=0.00)
    total_expense = Column(DECIMAL(10, 2), default=0.00)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

class WalletTransaction(Base):
    __tablename__ = "wallet_transactions"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    transaction_no = Column(String(64), unique=True, nullable=False, index=True)
    user_open_id = Column(String(128), nullable=False, index=True)
    transaction_type = Column(String(32), nullable=False, index=True)
    amount = Column(DECIMAL(10, 2), nullable=False)
    balance_before = Column(DECIMAL(10, 2), nullable=False)
    balance_after = Column(DECIMAL(10, 2), nullable=False)
    related_type = Column(String(32))
    related_id = Column(BigInteger, index=True)
    description = Column(String(512))
    status = Column(Integer, default=1)
    created_at = Column(TIMESTAMP, server_default=func.now(), index=True)
