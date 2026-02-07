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
│   └── tests/              # 测试
├── docs/                   # 📚 所有文档（安装、配置、故障排除等）
│   ├── README.md           # 文档索引
│   ├── 现在就开始.md        # 中文快速启动（推荐）
│   ├── START_HERE.md       # 英文快速启动
│   ├── 快速参考.md          # 命令速查表
│   ├── TROUBLESHOOTING.md  # 故障排除
│   └── ...                 # 其他文档
├── scripts/                # 🔧 所有脚本（启动、安装、数据库等）
│   ├── README.md           # 脚本说明
│   ├── run_dev.cmd         # 一键启动（推荐）
│   ├── setup.cmd           # 安装脚本
│   └── ...                 # 其他脚本
├── docker/                 # Docker 配置
│   ├── docker-compose.yml
│   └── Dockerfile
├── skill_hub/              # CLI 工具
│   └── cli.py              # uv run dev 等命令
├── .env                    # 环境变量配置
├── pyproject.toml          # UV 项目配置
├── create_tables.sql       # 数据库表结构
└── README.md               # 项目主文档（本文件）
```

## 快速开始

> 💡 **提示**: 所有文档已整理到 `docs/` 目录，所有脚本已整理到 `scripts/` 目录。

### 🚀 最简单的方式（推荐）

**方法 1: 使用一键启动脚本**
```cmd
scripts\run_dev.cmd
```

**方法 2: 使用 uv 命令**
```bash
# 确保在项目根目录
cd E:\projects\AIs\skill-creator

# 启动服务
uv run dev
```

访问 http://localhost:8000/docs 查看 API 文档。

**`uv run dev` 会自动：**
- ✅ 复制 `.env` 文件到 `backend` 目录
- ✅ 启动 MinIO 和 Redis（Docker）
- ✅ 启动 FastAPI 开发服务器

---

### 📚 详细文档

- **[现在就开始.md](docs/现在就开始.md)** - 中文快速启动指南（推荐新手）
- **[快速参考.md](docs/快速参考.md)** - 一页纸命令速查表
- **[TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)** - 遇到问题时查看
- **[docs/README.md](docs/README.md)** - 查看所有文档

### 🔧 脚本工具

- **[scripts/README.md](scripts/README.md)** - 查看所有可用脚本
- **`scripts\run_dev.cmd`** - 一键启动开发服务器
- **`scripts\setup.cmd`** - 首次安装设置
- **`scripts\init_local_db.cmd`** - 初始化数据库

---

### 首次安装步骤

```bash
# 1. 创建虚拟环境并安装
uv venv
uv pip install -e .

# 2. 配置环境变量
copy .env.example .env
# 编辑 .env，修改 MySQL 密码等配置

# 3. 初始化数据库
scripts\init_local_db.cmd
# 或使用: uv run db-init

# 4. 启动开发服务器
scripts\run_dev.cmd
# 或使用: uv run dev
```

就这么简单！

#### 1. 环境准备

**安装 uv（Python 包管理工具）**
```powershell
# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# 或使用 pip
pip install uv
```

**创建虚拟环境**
```bash
# 使用 uv 创建虚拟环境（比 venv 快 10 倍）
uv venv

# 激活虚拟环境
# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Windows (CMD)
.venv\Scripts\activate.bat
```

**安装依赖**
```bash
# 使用 uv 安装依赖（比 pip 快 10-100 倍）
uv pip install -e .

# 或安装开发依赖
uv pip install -e ".[dev]"

# 或从 requirements.txt 安装
uv pip install -r backend/requirements.txt
```

#### 2. 配置环境变量

创建 `.env` 文件：

```bash
# 复制模板
copy .env.example .env

# 编辑 .env 文件，填入实际配置
```

示例配置：
```env
DATABASE_URL=mysql+pymysql://root:root@localhost:3306/skill_hub

# 本地 MinIO 配置
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin123
MINIO_SECURE=False
MINIO_USE_HTTPS=False

# MinIO 存储桶
DEFAULT_FILE_BUCKET=skill-hub
MINIO_BUCKET_NAME_SD=sd-generated-images

SECRET_KEY=your-secret-key-change-in-production
```

**注意**: 项目使用本地 MinIO 服务（Docker）。

#### 3. 初始化数据库

```bash
# 启动 Docker 服务
docker-compose up -d

# 等待服务启动（约 10-20 秒）

# 初始化数据库
# Windows (PowerShell)
Get-Content create_tables.sql | docker exec -i skill-hub-mysql mysql -uroot -proot123 skill_hub

# 或使用 MySQL 客户端
mysql -h localhost -P 3306 -u skillhub -pskillhub123 skill_hub < create_tables.sql
```

#### 4. 启动服务

```bash
# 进入后端目录
cd backend

# 使用 uv 启动开发服务器
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 5. 访问服务

- API 文档: http://localhost:8000/docs
- API 根路径: http://localhost:8000
- MinIO 控制台: http://localhost:9001 (minioadmin / minioadmin123)

**注意**: 
- 本项目使用本地 MySQL 和本地 MinIO（Docker）
- 默认存储桶: `skill-hub`
- MinIO 数据存储在 Docker volume 中

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

### 使用 uv 命令（推荐）

```bash
# 启动开发服务器
uv run dev

# 初始化数据库
uv run db-init

# 重置数据库
uv run db-reset

# 运行测试
uv run pytest

# 格式化代码
uv run black backend/app
```

查看所有可用命令: [UV_COMMANDS.md](UV_COMMANDS.md)

### 使用 uv 管理依赖

```bash
# 安装新包
uv pip install package-name

# 安装指定版本
uv pip install package-name==1.0.0

# 卸载包
uv pip uninstall package-name

# 列出已安装的包
uv pip list

# 更新 requirements.txt
uv pip freeze > backend/requirements.txt
```

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
# 安装测试依赖
uv pip install -e ".[dev]"

# 运行所有测试
uv run pytest

# 运行特定测试
uv run pytest tests/test_skills.py

# 生成覆盖率报告
uv run pytest --cov=app tests/

# 代码格式化
uv run black backend/app

# 代码检查
uv run flake8 backend/app
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
