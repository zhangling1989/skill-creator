# 使用 uv 设置开发环境

## 前置条件

确保已安装 uv：
```bash
# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# 或使用 pip 安装
pip install uv
```

## 快速开始

### 1. 创建虚拟环境

```bash
# 使用 uv 创建虚拟环境（Python 3.11+）
uv venv

# 或指定 Python 版本
uv venv --python 3.11
```

### 2. 激活虚拟环境

```bash
# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Windows (CMD)
.venv\Scripts\activate.bat

# Linux/Mac
source .venv/bin/activate
```

### 3. 安装依赖

```bash
# 使用 uv 安装所有依赖（比 pip 快很多）
uv pip install -e .

# 或者安装开发依赖
uv pip install -e ".[dev]"

# 或者直接从 requirements.txt 安装
uv pip install -r backend/requirements.txt
```

### 4. 配置环境变量

```bash
# 复制环境变量模板
copy .env.example .env

# 编辑 .env 文件，填入实际配置
```

### 5. 初始化数据库

```bash
# 启动 Docker 服务（MySQL, MinIO, Redis）
docker-compose up -d

# 等待服务启动（约 10-20 秒）

# 执行数据库初始化脚本
# Windows (PowerShell)
Get-Content create_tables.sql | docker exec -i skill-hub-mysql mysql -uroot -proot123 skill_hub

# 或使用 MySQL 客户端
mysql -h localhost -P 3306 -u skillhub -pskillhub123 skill_hub < create_tables.sql
```

### 6. 启动开发服务器

```bash
# 进入后端目录
cd backend

# 启动 FastAPI 开发服务器
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 或者使用 Python 直接运行
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 7. 访问服务

- API 文档: http://localhost:8000/docs
- API 根路径: http://localhost:8000
- MinIO 控制台: http://localhost:9001 (用户名: minioadmin, 密码: minioadmin123)

## uv 常用命令

### 包管理

```bash
# 安装单个包
uv pip install fastapi

# 安装指定版本
uv pip install fastapi==0.109.0

# 卸载包
uv pip uninstall fastapi

# 列出已安装的包
uv pip list

# 冻结依赖到文件
uv pip freeze > requirements.txt

# 同步依赖（根据 pyproject.toml）
uv pip sync
```

### 虚拟环境管理

```bash
# 创建虚拟环境
uv venv

# 创建指定 Python 版本的虚拟环境
uv venv --python 3.11

# 删除虚拟环境
rmdir /s .venv  # Windows
rm -rf .venv    # Linux/Mac
```

### 运行脚本

```bash
# 使用 uv 运行 Python 脚本（自动使用虚拟环境）
uv run python script.py

# 运行 uvicorn
uv run uvicorn app.main:app --reload
```

## 项目结构

```
skill-hub/
├── .venv/                  # uv 创建的虚拟环境
├── backend/
│   ├── app/
│   │   ├── api/           # API 路由
│   │   ├── core/          # 核心配置
│   │   ├── models/        # 数据模型
│   │   ├── schemas/       # Pydantic 模型
│   │   ├── services/      # 业务逻辑
│   │   └── main.py        # 应用入口
│   └── requirements.txt
├── database/
│   └── create_tables.sql
├── docs/
├── .env                   # 环境变量（需创建）
├── .env.example          # 环境变量模板
├── pyproject.toml        # 项目配置（uv 使用）
└── docker-compose.yml
```

## 开发工作流

### 1. 每日开发

```bash
# 1. 激活虚拟环境
.venv\Scripts\Activate.ps1

# 2. 启动 Docker 服务
docker-compose up -d

# 3. 启动开发服务器
cd backend
uv run uvicorn app.main:app --reload
```

### 2. 添加新依赖

```bash
# 1. 使用 uv 安装
uv pip install new-package

# 2. 更新 pyproject.toml
# 手动添加到 dependencies 列表

# 3. 或更新 requirements.txt
uv pip freeze > backend/requirements.txt
```

### 3. 运行测试

```bash
# 安装测试依赖
uv pip install -e ".[dev]"

# 运行测试
uv run pytest

# 运行测试并生成覆盖率报告
uv run pytest --cov=app tests/
```

### 4. 代码格式化

```bash
# 使用 black 格式化代码
uv run black backend/app

# 使用 flake8 检查代码
uv run flake8 backend/app
```

## 常见问题

### Q: uv 安装速度慢？
A: uv 使用 Rust 编写，比 pip 快 10-100 倍。如果还是慢，可以配置国内镜像：
```bash
uv pip install -i https://pypi.tuna.tsinghua.edu.cn/simple package-name
```

### Q: 虚拟环境激活失败？
A: Windows PowerShell 可能需要修改执行策略：
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Q: 数据库连接失败？
A: 检查 Docker 服务是否启动：
```bash
docker-compose ps
```

### Q: 如何重置数据库？
A: 
```bash
# 停止并删除容器
docker-compose down -v

# 重新启动
docker-compose up -d

# 重新执行建表脚本
Get-Content create_tables.sql | docker exec -i skill-hub-mysql mysql -uroot -proot123 skill_hub
```

## 性能对比

uv vs pip 安装速度对比：

| 操作 | pip | uv | 提升 |
|------|-----|----|----|
| 安装 FastAPI | ~15s | ~1s | 15x |
| 安装所有依赖 | ~60s | ~5s | 12x |
| 创建虚拟环境 | ~10s | ~1s | 10x |

## 更多资源

- uv 官方文档: https://docs.astral.sh/uv/
- FastAPI 文档: https://fastapi.tiangolo.com/
- MinIO 文档: https://min.io/docs/
