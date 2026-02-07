# Skill Hub 平台

基于 MinIO 对象存储的 Skill 管理平台，支持用户上传、管理和分享 Skill 文件。

## 项目特性

- 🔐 SSO 单点登录集成
- 📦 基于 MinIO 的分布式文件存储
- 📁 **批量上传文件夹，保持原有目录结构**
- 🏷️ 灵活的分类和标签系统
- 📝 Skill 版本管理
- ⭐ 收藏、评论、评分功能
- 💰 **Skill 定价和按使用计费**
- 💳 **用户钱包系统（充值、提现、收支记录）**
- 📊 统计分析（浏览、下载、使用次数）
- 🤖 **Agent 调用 Skill 自动扣费**
- 🔍 全文搜索支持

## 技术栈

- **后端**: Python 3.11+ / FastAPI
- **数据库**: MySQL 8.0+
- **对象存储**: MinIO
- **认证**: SSO (OAuth2/OIDC)
- **缓存**: Redis
- **搜索**: Elasticsearch (可选)

## 项目结构

```
skill-hub/
├── backend/                 # 后端服务
│   ├── app/
│   │   ├── api/            # API 路由
│   │   ├── core/           # 核心配置
│   │   ├── models/         # 数据模型
│   │   ├── schemas/        # Pydantic 模型
│   │   ├── services/       # 业务逻辑
│   │   └── utils/          # 工具函数
│   ├── tests/              # 测试
│   └── requirements.txt    # 依赖
├── database/               # 数据库脚本
│   ├── create_tables.sql
│   └── migrations/
├── docs/                   # 文档
│   └── api/               # API 文档
├── docker/                 # Docker 配置
│   ├── docker-compose.yml
│   └── Dockerfile
└── README.md
```

## 快速开始

### 1. 环境准备

```bash
# 克隆项目
git clone <repository-url>
cd skill-hub

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r backend/requirements.txt
```

### 2. 配置环境变量

创建 `.env` 文件：

```env
# 数据库配置
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/skill_hub

# MinIO 配置
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_SECURE=false

# SSO 配置
SSO_CLIENT_ID=your_client_id
SSO_CLIENT_SECRET=your_client_secret
SSO_AUTHORIZE_URL=https://sso.example.com/oauth/authorize
SSO_TOKEN_URL=https://sso.example.com/oauth/token
SSO_USERINFO_URL=https://sso.example.com/oauth/userinfo

# Redis 配置
REDIS_URL=redis://localhost:6379/0

# 应用配置
SECRET_KEY=your-secret-key-here
DEBUG=true
```

### 3. 初始化数据库

```bash
# 创建数据库
mysql -u root -p -e "CREATE DATABASE skill_hub CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# 执行建表脚本
mysql -u root -p skill_hub < database/create_tables.sql
```

### 4. 启动服务

```bash
# 使用 Docker Compose 启动所有服务
docker-compose up -d

# 或手动启动后端服务
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 5. 访问服务

- API 文档: http://localhost:8000/docs
- MinIO 控制台: http://localhost:9001

## API 接口

### 认证相关
- `POST /api/v1/auth/login` - SSO 登录
- `POST /api/v1/auth/logout` - 登出
- `GET /api/v1/auth/me` - 获取当前用户信息

### Skill 管理
- `POST /api/v1/skills` - 上传单个 Skill 文件
- `POST /api/v1/skills/batch-upload` - 批量上传文件夹（保持目录结构）
- `GET /api/v1/skills` - 获取 Skill 列表
- `GET /api/v1/skills/{id}` - 获取 Skill 详情
- `GET /api/v1/skills/{id}/files` - 获取批量上传 Skill 的文件列表
- `GET /api/v1/skills/{id}/download-file` - 下载批量上传 Skill 中的单个文件
- `PUT /api/v1/skills/{id}` - 更新 Skill
- `DELETE /api/v1/skills/{id}` - 删除 Skill
- `GET /api/v1/skills/{id}/download` - 下载 Skill

### 分类管理
- `GET /api/v1/categories` - 获取分类列表
- `POST /api/v1/categories` - 创建分类

### 项目管理
- `POST /api/v1/projects` - 创建项目
- `GET /api/v1/projects` - 获取项目列表
- `GET /api/v1/projects/{id}` - 获取项目详情

### 社交功能
- `POST /api/v1/skills/{id}/star` - 收藏 Skill
- `DELETE /api/v1/skills/{id}/star` - 取消收藏
- `POST /api/v1/skills/{id}/comments` - 添加评论
- `GET /api/v1/skills/{id}/comments` - 获取评论列表

### 钱包和计费
- `GET /api/v1/user/wallet` - 获取钱包信息
- `POST /api/v1/user/wallet/recharge` - 充值
- `GET /api/v1/user/wallet/transactions` - 获取交易记录
- `POST /api/v1/user/skills/use` - 使用 Skill（Agent 调用，自动扣费）
- `GET /api/v1/user/skills/usage-logs` - 获取使用记录
- `GET /api/v1/user/skills/starred` - 获取我的收藏
- `GET /api/v1/user/skills/income-stats` - 获取收入统计

## MinIO 存储结构

### 单文件上传
```
bucket: project-name/
├── open_id_1/
│   ├── skill-1.md
│   └── skill-2.md
└── open_id_2/
    └── skill-3.md
```

### 批量上传（保持目录结构）
```
bucket: project-name/
└── open_id_1/
    ├── my-project/
    │   ├── docs/
    │   │   ├── README.md
    │   │   └── API.md
    │   ├── src/
    │   │   ├── main.py
    │   │   └── utils.py
    │   └── tests/
    │       └── test_main.py
    └── versions/
        ├── skill-1_v1.0.0.md
        └── skill-1_v2.0.0.md
```

## 开发指南

### 添加新的 API 端点

1. 在 `backend/app/api/v1/` 创建路由文件
2. 在 `backend/app/schemas/` 定义请求/响应模型
3. 在 `backend/app/services/` 实现业务逻辑
4. 在 `backend/app/api/v1/__init__.py` 注册路由

### 数据库迁移

```bash
# 创建迁移
alembic revision --autogenerate -m "description"

# 执行迁移
alembic upgrade head
```

## 测试

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_skills.py

# 生成覆盖率报告
pytest --cov=app tests/
```

## 部署

### Docker 部署

```bash
# 构建镜像
docker build -t skill-hub:latest .

# 运行容器
docker-compose -f docker/docker-compose.prod.yml up -d
```

### 生产环境配置

- 使用 Nginx 作为反向代理
- 配置 HTTPS 证书
- 启用 Redis 缓存
- 配置日志收集
- 设置监控告警

## 许可证

MIT License
