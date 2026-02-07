# 使用 uv 命令启动项目

## 快速开始

### 1. 首次设置

```bash
# 创建虚拟环境
uv venv

# 激活虚拟环境（可选，使用 uv run 可跳过）
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
# Windows (CMD)
.venv\Scripts\activate.bat

# 安装项目（可编辑模式）
uv pip install -e .

# 配置环境变量
copy .env.example .env
# 编辑 .env 文件，修改数据库密码等配置
```

### 2. 启动开发服务器

```bash
# 使用 uv run（推荐，自动处理一切）
uv run dev
```

就这么简单！这个命令会：
- ✅ 自动复制 `.env` 文件到 `backend` 目录
- ✅ 自动检查并启动 Docker 服务（MinIO + Redis）
- ✅ 启动 FastAPI 开发服务器
- ✅ 自动重载代码变更

## 所有可用命令

### 开发相关

```bash
# 启动开发服务器（自动重载）
uv run dev

# 启动生产服务器（多进程）
uv run start
```

### 数据库相关

```bash
# 初始化数据库
uv run db-init

# 重置数据库（删除所有数据）
uv run db-reset
```

### 测试相关

```bash
# 运行测试
uv run pytest

# 运行测试并生成覆盖率报告
uv run pytest --cov=backend/app tests/

# 运行特定测试文件
uv run pytest tests/test_skills.py
```

### 代码质量

```bash
# 格式化代码
uv run black backend/app

# 检查代码风格
uv run flake8 backend/app

# 类型检查
uv run mypy backend/app
```

### 依赖管理

```bash
# 安装新包
uv pip install package-name

# 安装开发依赖
uv pip install -e ".[dev]"

# 列出已安装的包
uv pip list

# 更新 requirements.txt
uv pip freeze > backend/requirements.txt
```

## 常用工作流

### 每日开发

```bash
# 一条命令启动所有服务
uv run dev

# 访问 http://localhost:8000/docs
```

**提示**: 首次运行会下载 Docker 镜像，需要等待几分钟。之后启动会很快。

### 添加新功能

```bash
# 1. 创建新分支
git checkout -b feature/new-feature

# 2. 开发代码...

# 3. 格式化代码
uv run black backend/app

# 4. 运行测试
uv run pytest

# 5. 提交代码
git add .
git commit -m "Add new feature"
```

### 数据库操作

```bash
# 初始化数据库（首次使用或重置后）
uv run db-init

# 会提示选择:
# 1. 本地 MySQL (localhost:3306) - 推荐
# 2. Docker MySQL (localhost:3307)

# 重置数据库（清空所有数据）
uv run db-reset
```

## 为什么使用 uv run？

### 优势

1. **自动使用虚拟环境**: 不需要手动激活虚拟环境
2. **速度快**: 比 pip 快 10-100 倍
3. **简洁**: 一个命令搞定所有操作
4. **可靠**: 确保使用正确的 Python 环境

### 对比

```bash
# 传统方式
.venv\Scripts\activate.bat
python -m uvicorn backend.app.main:app --reload

# uv 方式
uv run dev
```

## 配置说明

所有命令都在 `pyproject.toml` 中定义：

```toml
[project.scripts]
dev = "skill_hub.cli:dev"           # 开发服务器
start = "skill_hub.cli:start"       # 生产服务器
db-init = "skill_hub.cli:db_init"   # 初始化数据库
db-reset = "skill_hub.cli:db_reset" # 重置数据库
```

## 自定义命令

你可以在 `skill_hub/cli.py` 中添加自己的命令：

```python
def my_command():
    """我的自定义命令"""
    print("执行自定义操作...")
    # 你的代码

# 然后在 pyproject.toml 中注册
[project.scripts]
my-cmd = "skill_hub.cli:my_command"
```

使用：
```bash
uv run my-cmd
```

## 环境变量

命令会自动读取 `.env` 文件中的配置：

```env
DATABASE_URL=mysql+pymysql://skillhub:skillhub123@localhost:3306/skill_hub
MINIO_ENDPOINT=8.133.242.214:19000
MINIO_ACCESS_KEY=root
MINIO_SECRET_KEY=root10kv
```

## 故障排除

### 命令找不到

```bash
# 确保已安装项目
uv pip install -e .

# 检查安装
uv pip list | grep skill-hub
```

### 虚拟环境问题

```bash
# 删除并重建虚拟环境
rmdir /s .venv  # Windows
uv venv
uv pip install -e .
```

### Docker 服务未启动

```bash
# 手动启动 Docker 服务
docker-compose up -d

# 检查状态
docker-compose ps
```

## 完整示例

```bash
# 1. 克隆项目
git clone <repository-url>
cd skill-hub

# 2. 创建虚拟环境
uv venv

# 3. 安装项目
uv pip install -e .

# 4. 配置环境变量
copy .env.example .env

# 5. 启动 Docker
docker-compose up -d

# 6. 初始化数据库
uv run db-init

# 7. 启动开发服务器
uv run dev

# 8. 访问 API 文档
# http://localhost:8000/docs
```

## 更多资源

- uv 文档: https://docs.astral.sh/uv/
- FastAPI 文档: https://fastapi.tiangolo.com/
- 项目 README: [README.md](README.md)
