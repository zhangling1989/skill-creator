# Skill 定价和计费系统使用指南

## 功能概述

Skill Hub 支持 Skill 定价和按使用计费功能。用户可以收藏 Skill，当 Agent 使用收藏的 Skill 时自动扣费。

## 核心概念

### 1. Skill 定价模式

- **free**: 免费 Skill，任何人都可以免费使用
- **per_use**: 按次计费，每次使用收取固定费用
- **subscription**: 订阅模式（预留，暂未实现）

### 2. 使用流程

```
用户浏览 Skill → 收藏 Skill → Agent 调用 Skill → 自动扣费 → 作者获得收入
```

### 3. 计费规则

- 用户收藏 Skill 时不收费
- 只有 Agent 实际使用 Skill 时才收费
- 使用自己创建的 Skill 不收费
- 免费 Skill 不收费

## 数据库表结构

### Skills 表（新增字段）

```sql
price DECIMAL(10,2) DEFAULT 0.00  -- Skill 价格
pricing_model VARCHAR(32) DEFAULT 'per_use'  -- 计费模式
usage_count INT DEFAULT 0  -- 使用次数统计
```

### 用户钱包表 (user_wallets)

```sql
user_open_id VARCHAR(128)  -- 用户 ID
balance DECIMAL(10,2)  -- 当前余额
frozen_balance DECIMAL(10,2)  -- 冻结金额
total_income DECIMAL(10,2)  -- 总收入
total_expense DECIMAL(10,2)  -- 总支出
```

### 使用记录表 (skill_usage_logs)

```sql
skill_id BIGINT  -- Skill ID
user_open_id VARCHAR(128)  -- 使用者
agent_id VARCHAR(128)  -- Agent ID
charge_amount DECIMAL(10,2)  -- 收费金额
status TINYINT  -- 状态：1-成功，0-失败
```

### 交易记录表 (wallet_transactions)

```sql
transaction_no VARCHAR(64)  -- 交易流水号
transaction_type VARCHAR(32)  -- 类型：recharge, income, expense
amount DECIMAL(10,2)  -- 交易金额
balance_before DECIMAL(10,2)  -- 交易前余额
balance_after DECIMAL(10,2)  -- 交易后余额
```

## API 接口使用

### 1. 上传 Skill 并设置价格

```bash
curl -X POST "http://localhost:8000/api/v1/skills" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@skill.md" \
  -F "skill_name=我的 Skill" \
  -F "description=这是一个付费 Skill" \
  -F "category_id=1" \
  -F "project_id=1" \
  -F "price=5.00" \
  -F "pricing_model=per_use"
```

### 2. 收藏 Skill

```bash
curl -X POST "http://localhost:8000/api/v1/skills/123/star" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

响应：
```json
{
  "message": "收藏成功"
}
```

### 3. 获取我的收藏

```bash
curl -X GET "http://localhost:8000/api/v1/user/skills/starred" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

响应：
```json
[
  {
    "id": 123,
    "skill_name": "数据分析工具",
    "price": 5.00,
    "pricing_model": "per_use",
    "owner_open_id": "author_123"
  }
]
```

### 4. 查看钱包余额

```bash
curl -X GET "http://localhost:8000/api/v1/user/wallet" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

响应：
```json
{
  "user_open_id": "user_123",
  "balance": 100.00,
  "frozen_balance": 0.00,
  "total_income": 50.00,
  "total_expense": 20.00,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

### 5. 充值

```bash
curl -X POST "http://localhost:8000/api/v1/user/wallet/recharge" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 100.00,
    "description": "账户充值"
  }'
```

响应：
```json
{
  "success": true,
  "message": "充值成功",
  "amount": 100.00,
  "balance": 200.00
}
```

### 6. Agent 使用 Skill（自动扣费）

```bash
curl -X POST "http://localhost:8000/api/v1/user/skills/use" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "skill_id": 123,
    "agent_id": "agent_001",
    "usage_type": "agent_call",
    "request_data": {
      "query": "分析数据",
      "params": {}
    }
  }'
```

响应（成功）：
```json
{
  "success": true,
  "message": "收费成功",
  "charge_amount": 5.00,
  "balance": 95.00,
  "usage_log_id": 456
}
```

响应（余额不足）：
```json
{
  "success": false,
  "message": "余额不足",
  "required": 5.00,
  "balance": 2.00
}
```

### 7. 查看使用记录

```bash
curl -X GET "http://localhost:8000/api/v1/user/skills/usage-logs?page=1&page_size=20" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

响应：
```json
[
  {
    "id": 456,
    "skill_id": 123,
    "user_open_id": "user_123",
    "agent_id": "agent_001",
    "usage_type": "agent_call",
    "charge_amount": 5.00,
    "status": 1,
    "created_at": "2024-01-01T12:00:00"
  }
]
```

### 8. 查看交易记录

```bash
curl -X GET "http://localhost:8000/api/v1/user/wallet/transactions?page=1&page_size=20" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

响应：
```json
{
  "total": 10,
  "page": 1,
  "page_size": 20,
  "items": [
    {
      "id": 1,
      "transaction_no": "TXN20240101120000abcd1234",
      "user_open_id": "user_123",
      "transaction_type": "expense",
      "amount": 5.00,
      "balance_before": 100.00,
      "balance_after": 95.00,
      "related_type": "skill_usage",
      "related_id": 123,
      "description": "使用 Skill: 数据分析工具",
      "status": 1,
      "created_at": "2024-01-01T12:00:00"
    }
  ]
}
```

### 9. 查看收入统计（Skill 作者）

```bash
curl -X GET "http://localhost:8000/api/v1/user/skills/income-stats" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

响应：
```json
{
  "total_income": 150.00,
  "current_balance": 150.00,
  "skills": [
    {
      "skill_id": 123,
      "skill_name": "数据分析工具",
      "price": 5.00,
      "pricing_model": "per_use",
      "usage_count": 30,
      "total_income": 150.00
    }
  ]
}
```

## Python 客户端示例

### 完整的使用流程

```python
import requests

class SkillHubClient:
    def __init__(self, base_url, token):
        self.base_url = base_url
        self.headers = {"Authorization": f"Bearer {token}"}
    
    def get_wallet(self):
        """获取钱包信息"""
        response = requests.get(
            f"{self.base_url}/api/v1/user/wallet",
            headers=self.headers
        )
        return response.json()
    
    def recharge(self, amount):
        """充值"""
        response = requests.post(
            f"{self.base_url}/api/v1/user/wallet/recharge",
            headers=self.headers,
            params={"amount": amount}
        )
        return response.json()
    
    def star_skill(self, skill_id):
        """收藏 Skill"""
        response = requests.post(
            f"{self.base_url}/api/v1/skills/{skill_id}/star",
            headers=self.headers
        )
        return response.json()
    
    def get_starred_skills(self):
        """获取我的收藏"""
        response = requests.get(
            f"{self.base_url}/api/v1/user/skills/starred",
            headers=self.headers
        )
        return response.json()
    
    def use_skill(self, skill_id, agent_id, request_data=None):
        """使用 Skill（Agent 调用）"""
        response = requests.post(
            f"{self.base_url}/api/v1/user/skills/use",
            headers=self.headers,
            json={
                "skill_id": skill_id,
                "agent_id": agent_id,
                "usage_type": "agent_call",
                "request_data": request_data or {}
            }
        )
        return response.json()
    
    def get_usage_logs(self, page=1, page_size=20):
        """获取使用记录"""
        response = requests.get(
            f"{self.base_url}/api/v1/user/skills/usage-logs",
            headers=self.headers,
            params={"page": page, "page_size": page_size}
        )
        return response.json()
    
    def get_income_stats(self):
        """获取收入统计"""
        response = requests.get(
            f"{self.base_url}/api/v1/user/skills/income-stats",
            headers=self.headers
        )
        return response.json()

# 使用示例
client = SkillHubClient("http://localhost:8000", "your_token")

# 1. 查看钱包
wallet = client.get_wallet()
print(f"当前余额: {wallet['balance']}")

# 2. 充值
if wallet['balance'] < 10:
    result = client.recharge(100)
    print(f"充值成功，新余额: {result['balance']}")

# 3. 收藏 Skill
client.star_skill(123)
print("收藏成功")

# 4. 查看我的收藏
starred = client.get_starred_skills()
print(f"我收藏了 {len(starred)} 个 Skill")

# 5. Agent 使用 Skill
result = client.use_skill(
    skill_id=123,
    agent_id="agent_001",
    request_data={"query": "分析数据"}
)

if result['success']:
    print(f"使用成功，扣费: {result['charge_amount']}")
    print(f"剩余余额: {result['balance']}")
else:
    print(f"使用失败: {result['message']}")

# 6. 查看使用记录
logs = client.get_usage_logs()
print(f"使用记录: {logs}")

# 7. 查看收入统计（作者）
stats = client.get_income_stats()
print(f"总收入: {stats['total_income']}")
```

## Agent 集成示例

### Agent 调用 Skill 的流程

```python
class Agent:
    def __init__(self, skill_hub_client, agent_id):
        self.client = skill_hub_client
        self.agent_id = agent_id
    
    def execute_skill(self, skill_id, params):
        """执行 Skill"""
        # 1. 调用计费接口
        result = self.client.use_skill(
            skill_id=skill_id,
            agent_id=self.agent_id,
            request_data=params
        )
        
        if not result['success']:
            raise Exception(f"Skill 使用失败: {result['message']}")
        
        # 2. 执行实际的 Skill 逻辑
        # 这里是 Agent 的具体实现
        skill_result = self._run_skill_logic(skill_id, params)
        
        return {
            "charge_amount": result['charge_amount'],
            "balance": result['balance'],
            "result": skill_result
        }
    
    def _run_skill_logic(self, skill_id, params):
        """实际的 Skill 执行逻辑"""
        # Agent 的具体实现
        pass

# 使用
agent = Agent(client, "agent_001")
result = agent.execute_skill(123, {"query": "分析数据"})
```

## 注意事项

1. **余额检查**: Agent 调用前应检查用户余额是否充足
2. **错误处理**: 余额不足时应提示用户充值
3. **免费 Skill**: 免费 Skill 不会扣费，但会记录使用日志
4. **自己的 Skill**: 使用自己创建的 Skill 不收费
5. **交易记录**: 所有交易都有完整的流水记录
6. **收入分配**: Skill 被使用时，费用直接进入作者钱包

## 计费流程图

```
┌─────────────┐
│ Agent 调用  │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│ 检查用户是否收藏 │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│ 检查 Skill 定价  │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│ 检查用户余额     │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│ 扣除用户余额     │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│ 增加作者收入     │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│ 记录使用日志     │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│ 返回结果         │
└─────────────────┘
```

## 数据统计

系统会自动统计：
- 每个 Skill 的使用次数
- 每个 Skill 的总收入
- 用户的总支出
- 作者的总收入
- 详细的交易流水
