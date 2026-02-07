from sqlalchemy.orm import Session
from app.models.skill import UserWallet, WalletTransaction, Skill, SkillUsageLog
from decimal import Decimal
import uuid
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class WalletService:
    
    @staticmethod
    def get_or_create_wallet(db: Session, user_open_id: str) -> UserWallet:
        """获取或创建用户钱包"""
        wallet = db.query(UserWallet).filter(
            UserWallet.user_open_id == user_open_id
        ).first()
        
        if not wallet:
            wallet = UserWallet(user_open_id=user_open_id)
            db.add(wallet)
            db.commit()
            db.refresh(wallet)
            logger.info(f"创建钱包: {user_open_id}")
        
        return wallet
    
    @staticmethod
    def generate_transaction_no() -> str:
        """生成交易流水号"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        return f"TXN{timestamp}{unique_id}"
    
    @staticmethod
    def charge_for_skill_usage(
        db: Session,
        skill_id: int,
        user_open_id: str,
        agent_id: str = None,
        usage_type: str = "agent_call",
        request_data: dict = None
    ) -> dict:
        """为 Skill 使用收费
        
        Args:
            db: 数据库会话
            skill_id: Skill ID
            user_open_id: 使用者 open_id
            agent_id: Agent ID
            usage_type: 使用类型
            request_data: 请求数据
            
        Returns:
            包含收费结果的字典
        """
        # 获取 Skill 信息
        skill = db.query(Skill).filter(Skill.id == skill_id).first()
        if not skill:
            return {"success": False, "message": "Skill 不存在"}
        
        # 检查定价模式
        if skill.pricing_model == "free":
            charge_amount = Decimal("0.00")
        else:
            charge_amount = Decimal(str(skill.price))
        
        # 如果是自己的 Skill，不收费
        if skill.owner_open_id == user_open_id:
            charge_amount = Decimal("0.00")
        
        # 获取用户钱包
        user_wallet = WalletService.get_or_create_wallet(db, user_open_id)
        
        # 检查余额
        if charge_amount > 0 and user_wallet.balance < charge_amount:
            # 记录失败的使用日志
            usage_log = SkillUsageLog(
                skill_id=skill_id,
                user_open_id=user_open_id,
                agent_id=agent_id,
                usage_type=usage_type,
                charge_amount=float(charge_amount),
                status=0,  # 失败
                request_data=request_data
            )
            db.add(usage_log)
            db.commit()
            
            return {
                "success": False,
                "message": "余额不足",
                "required": float(charge_amount),
                "balance": float(user_wallet.balance)
            }
        
        # 扣费
        if charge_amount > 0:
            balance_before = user_wallet.balance
            user_wallet.balance -= charge_amount
            user_wallet.total_expense += charge_amount
            balance_after = user_wallet.balance
            
            # 创建支出交易记录
            expense_transaction = WalletTransaction(
                transaction_no=WalletService.generate_transaction_no(),
                user_open_id=user_open_id,
                transaction_type="expense",
                amount=float(charge_amount),
                balance_before=float(balance_before),
                balance_after=float(balance_after),
                related_type="skill_usage",
                related_id=skill_id,
                description=f"使用 Skill: {skill.skill_name}",
                status=1
            )
            db.add(expense_transaction)
            
            # 给 Skill 作者增加收入
            author_wallet = WalletService.get_or_create_wallet(db, skill.owner_open_id)
            author_balance_before = author_wallet.balance
            author_wallet.balance += charge_amount
            author_wallet.total_income += charge_amount
            author_balance_after = author_wallet.balance
            
            # 创建收入交易记录
            income_transaction = WalletTransaction(
                transaction_no=WalletService.generate_transaction_no(),
                user_open_id=skill.owner_open_id,
                transaction_type="income",
                amount=float(charge_amount),
                balance_before=float(author_balance_before),
                balance_after=float(author_balance_after),
                related_type="skill_usage",
                related_id=skill_id,
                description=f"Skill 被使用: {skill.skill_name}",
                status=1
            )
            db.add(income_transaction)
        
        # 记录使用日志
        usage_log = SkillUsageLog(
            skill_id=skill_id,
            user_open_id=user_open_id,
            agent_id=agent_id,
            usage_type=usage_type,
            charge_amount=float(charge_amount),
            status=1,  # 成功
            request_data=request_data
        )
        db.add(usage_log)
        
        # 更新 Skill 使用次数
        skill.usage_count += 1
        
        db.commit()
        
        logger.info(f"Skill 使用收费成功: skill_id={skill_id}, user={user_open_id}, amount={charge_amount}")
        
        return {
            "success": True,
            "message": "收费成功",
            "charge_amount": float(charge_amount),
            "balance": float(user_wallet.balance),
            "usage_log_id": usage_log.id
        }
    
    @staticmethod
    def recharge(db: Session, user_open_id: str, amount: float, description: str = None) -> dict:
        """充值"""
        if amount <= 0:
            return {"success": False, "message": "充值金额必须大于0"}
        
        wallet = WalletService.get_or_create_wallet(db, user_open_id)
        
        balance_before = wallet.balance
        wallet.balance += Decimal(str(amount))
        balance_after = wallet.balance
        
        transaction = WalletTransaction(
            transaction_no=WalletService.generate_transaction_no(),
            user_open_id=user_open_id,
            transaction_type="recharge",
            amount=amount,
            balance_before=float(balance_before),
            balance_after=float(balance_after),
            description=description or "账户充值",
            status=1
        )
        
        db.add(transaction)
        db.commit()
        
        logger.info(f"充值成功: user={user_open_id}, amount={amount}")
        
        return {
            "success": True,
            "message": "充值成功",
            "amount": amount,
            "balance": float(wallet.balance)
        }
    
    @staticmethod
    def get_user_starred_skills(db: Session, user_open_id: str):
        """获取用户收藏的 Skill 列表"""
        from app.models.skill import SkillStar
        
        starred = db.query(Skill).join(
            SkillStar, Skill.id == SkillStar.skill_id
        ).filter(
            SkillStar.user_open_id == user_open_id,
            Skill.status == 1
        ).all()
        
        return starred

wallet_service = WalletService()
