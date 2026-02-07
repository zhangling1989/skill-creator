# Skill Hub 平台数据库设计

## 系统架构说明

- **存储方案**: MinIO 对象存储
- **桶结构**: `项目名称/open_id/skill文件.md`
- **认证方式**: SSO 单点登录

## 数据库表设计

### 1. 用户表 (users)

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | BIGINT | PRIMARY KEY, AUTO_INCREMENT | 用户ID |
| open_id | VARCHAR(128) | UNIQUE, NOT NULL, INDEX | SSO系统的open_id |
| username | VARCHAR(64) | NOT NULL | 用户名 |
| email | VARCHAR(128) | | 邮箱 |
| avatar_url | VARCHAR(512) | | 头像URL |
| status | TINYINT | DEFAULT 1 | 状态: 1-正常, 0-禁用 |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | 更新时间 |

### 2. 项目表 (projects)

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | BIGINT | PRIMARY KEY, AUTO_INCREMENT | 项目ID |
| project_name | VARCHAR(128) | UNIQUE, NOT NULL, INDEX | 项目名称(对应MinIO桶名) |
| display_name | VARCHAR(256) | NOT NULL | 项目显示名称 |
| description | TEXT | | 项目描述 |
| owner_id | BIGINT | NOT NULL, INDEX, FOREIGN KEY | 项目所有者ID |
| bucket_name | VARCHAR(128) | UNIQUE, NOT NULL | MinIO桶名 |
| is_public | TINYINT | DEFAULT 0 | 是否公开: 1-公开, 0-私有 |
| status | TINYINT | DEFAULT 1 | 状态: 1-正常, 0-禁用 |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | 更新时间 |

### 3. Skill分类表 (skill_categories)

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | BIGINT | PRIMARY KEY, AUTO_INCREMENT | 分类ID |
| category_name | VARCHAR(64) | UNIQUE, NOT NULL | 分类名称 |
| parent_id | BIGINT | INDEX, DEFAULT 0 | 父分类ID, 0表示顶级分类 |
| description | VARCHAR(512) | | 分类描述 |
| icon | VARCHAR(256) | | 分类图标 |
| sort_order | INT | DEFAULT 0 | 排序顺序 |
| status | TINYINT | DEFAULT 1 | 状态: 1-启用, 0-禁用 |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | 更新时间 |

### 4. Skill表 (skills) - 核心表

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | BIGINT | PRIMARY KEY, AUTO_INCREMENT | Skill ID |
| skill_name | VARCHAR(256) | NOT NULL, INDEX | Skill名称 |
| slug | VARCHAR(256) | NOT NULL, INDEX | URL友好的标识符 |
| description | TEXT | | Skill描述 |
| category_id | BIGINT | NOT NULL, INDEX, FOREIGN KEY | 分类ID |
| project_id | BIGINT | NOT NULL, INDEX, FOREIGN KEY | 所属项目ID |
| owner_open_id | VARCHAR(128) | NOT NULL, INDEX | 上传者的open_id |
| file_path | VARCHAR(1024) | NOT NULL | MinIO中的完整路径 |
| file_name | VARCHAR(256) | NOT NULL | 文件名 |
| file_size | BIGINT | | 文件大小(字节) |
| file_hash | VARCHAR(64) | INDEX | 文件MD5/SHA256哈希值 |
| version | VARCHAR(32) | DEFAULT '1.0.0' | 版本号 |
| tags | JSON | | 标签数组 |
| metadata | JSON | | 其他元数据 |
| price | DECIMAL(10,2) | DEFAULT 0.00 | Skill价格(元) |
| pricing_model | VARCHAR(32) | DEFAULT 'per_use' | 计费模式: free-免费, per_use-按次, subscription-订阅 |
| view_count | INT | DEFAULT 0 | 浏览次数 |
| download_count | INT | DEFAULT 0 | 下载次数 |
| star_count | INT | DEFAULT 0 | 收藏次数 |
| usage_count | INT | DEFAULT 0 | 使用次数 |
| is_public | TINYINT | DEFAULT 1 | 是否公开: 1-公开, 0-私有 |
| status | TINYINT | DEFAULT 1 | 状态: 1-正常, 0-已删除, 2-审核中 |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP, INDEX | 创建时间 |
| updated_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | 更新时间 |

**复合索引**:
- `idx_project_owner` (project_id, owner_open_id)
- `idx_category_status` (category_id, status)
- `idx_owner_created` (owner_open_id, created_at DESC)

### 5. Skill版本历史表 (skill_versions)

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | BIGINT | PRIMARY KEY, AUTO_INCREMENT | 版本ID |
| skill_id | BIGINT | NOT NULL, INDEX, FOREIGN KEY | Skill ID |
| version | VARCHAR(32) | NOT NULL | 版本号 |
| file_path | VARCHAR(1024) | NOT NULL | 该版本的文件路径 |
| file_hash | VARCHAR(64) | | 文件哈希值 |
| change_log | TEXT | | 变更日志 |
| created_by | VARCHAR(128) | NOT NULL | 创建者open_id |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | 创建时间 |

### 6. Skill收藏表 (skill_stars)

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | BIGINT | PRIMARY KEY, AUTO_INCREMENT | 收藏ID |
| skill_id | BIGINT | NOT NULL, INDEX, FOREIGN KEY | Skill ID |
| user_open_id | VARCHAR(128) | NOT NULL, INDEX | 用户open_id |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | 收藏时间 |

**唯一索引**: `unique_star` (skill_id, user_open_id)

### 7. Skill使用记录表 (skill_usage_logs)

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | BIGINT | PRIMARY KEY, AUTO_INCREMENT | 使用记录ID |
| skill_id | BIGINT | NOT NULL, INDEX, FOREIGN KEY | Skill ID |
| user_open_id | VARCHAR(128) | NOT NULL, INDEX | 使用者open_id |
| agent_id | VARCHAR(128) | INDEX | Agent ID（调用方标识） |
| usage_type | VARCHAR(32) | DEFAULT 'agent_call' | 使用类型: agent_call, api_call |
| charge_amount | DECIMAL(10,2) | DEFAULT 0.00 | 本次收费金额 |
| status | TINYINT | DEFAULT 1 | 状态: 1-成功, 0-失败, 2-待支付 |
| request_data | JSON | | 请求数据 |
| response_data | JSON | | 响应数据 |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP, INDEX | 使用时间 |

**索引**:
- `idx_user_created` (user_open_id, created_at DESC)
- `idx_skill_created` (skill_id, created_at DESC)

### 8. 用户钱包表 (user_wallets)

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | BIGINT | PRIMARY KEY, AUTO_INCREMENT | 钱包ID |
| user_open_id | VARCHAR(128) | UNIQUE, NOT NULL, INDEX | 用户open_id |
| balance | DECIMAL(10,2) | DEFAULT 0.00 | 余额 |
| frozen_balance | DECIMAL(10,2) | DEFAULT 0.00 | 冻结金额 |
| total_income | DECIMAL(10,2) | DEFAULT 0.00 | 总收入 |
| total_expense | DECIMAL(10,2) | DEFAULT 0.00 | 总支出 |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | 更新时间 |

### 9. 钱包交易记录表 (wallet_transactions)

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | BIGINT | PRIMARY KEY, AUTO_INCREMENT | 交易ID |
| transaction_no | VARCHAR(64) | UNIQUE, NOT NULL, INDEX | 交易流水号 |
| user_open_id | VARCHAR(128) | NOT NULL, INDEX | 用户open_id |
| transaction_type | VARCHAR(32) | NOT NULL, INDEX | 交易类型: recharge-充值, withdraw-提现, income-收入, expense-支出 |
| amount | DECIMAL(10,2) | NOT NULL | 交易金额 |
| balance_before | DECIMAL(10,2) | NOT NULL | 交易前余额 |
| balance_after | DECIMAL(10,2) | NOT NULL | 交易后余额 |
| related_type | VARCHAR(32) | | 关联类型: skill_usage, skill_sale |
| related_id | BIGINT | INDEX | 关联ID |
| description | VARCHAR(512) | | 交易描述 |
| status | TINYINT | DEFAULT 1 | 状态: 1-成功, 0-失败, 2-处理中 |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP, INDEX | 交易时间 |

### 10. Skill评论表 (skill_comments)

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | BIGINT | PRIMARY KEY, AUTO_INCREMENT | 评论ID |
| skill_id | BIGINT | NOT NULL, INDEX, FOREIGN KEY | Skill ID |
| user_open_id | VARCHAR(128) | NOT NULL, INDEX | 评论者open_id |
| parent_id | BIGINT | DEFAULT 0 | 父评论ID, 0表示顶级评论 |
| content | TEXT | NOT NULL | 评论内容 |
| rating | TINYINT | | 评分(1-5) |
| status | TINYINT | DEFAULT 1 | 状态: 1-正常, 0-已删除 |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | 更新时间 |

### 11. 操作日志表 (operation_logs)

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | BIGINT | PRIMARY KEY, AUTO_INCREMENT | 日志ID |
| user_open_id | VARCHAR(128) | NOT NULL, INDEX | 操作者open_id |
| operation_type | VARCHAR(32) | NOT NULL, INDEX | 操作类型: upload, download, delete, update |
| resource_type | VARCHAR(32) | NOT NULL | 资源类型: skill, project |
| resource_id | BIGINT | NOT NULL | 资源ID |
| ip_address | VARCHAR(64) | | IP地址 |
| user_agent | VARCHAR(512) | | 用户代理 |
| details | JSON | | 操作详情 |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP, INDEX | 操作时间 |

## MinIO 路径结构

```
bucket_name (项目名称)
└── open_id (用户ID)
    ├── skill_1.md
    ├── skill_2.md
    └── versions/
        ├── skill_1_v1.0.0.md
        └── skill_1_v2.0.0.md
```

## 关键设计说明

1. **存储分离**: 文件存储在 MinIO，元数据存储在数据库
2. **版本控制**: 支持 Skill 的版本管理
3. **权限控制**: 通过 is_public 字段控制访问权限
4. **统计信息**: 记录浏览、下载、收藏、使用等统计数据
5. **审计日志**: 完整的操作日志记录
6. **分类体系**: 支持多级分类
7. **标签系统**: 使用 JSON 字段存储灵活的标签
8. **文件校验**: 通过 file_hash 防止重复上传和验证文件完整性
9. **定价模式**: 支持免费、按次计费、订阅等多种模式
10. **收藏机制**: 用户收藏后可在"我的收藏"中使用
11. **使用计费**: Agent 调用时自动记录使用并扣费
12. **钱包系统**: 完整的充值、提现、收支记录

## 计费流程

### 用户收藏 Skill
1. 用户浏览 Skill 市场
2. 点击收藏按钮（免费操作）
3. Skill 添加到"我的收藏"
4. 此时不产生费用

### Agent 使用 Skill 并计费
1. Agent 调用用户收藏的 Skill
2. 系统检查用户钱包余额
3. 根据 Skill 定价扣费
4. 记录使用日志（skill_usage_logs）
5. 创建钱包交易记录（wallet_transactions）
6. Skill 作者获得收入
7. 更新 Skill 使用次数统计

## 索引优化建议

- 为高频查询字段添加索引
- 使用复合索引优化多条件查询
- 定期分析慢查询并优化
- 考虑对大表进行分区(按时间或项目)
