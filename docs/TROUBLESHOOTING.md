# 🔧 故障排除指南

## 目录
- [运行目录错误](#运行目录错误)
- [环境变量加载失败](#环境变量加载失败)
- [Docker 服务问题](#docker-服务问题)
- [数据库连接问题](#数据库连接问题)
- [端口冲突](#端口冲突)

---

## 运行目录错误

### 症状
```
E:\projects\AIs\skill-creator\backend> uv run dev
open E:\projects\AIs\skill-creator\backend\docker-compose.simple.yml: The system cannot find the file specified.
```

### 原因
在 `backend` 目录运行命令，但 `docker-compose.simple.yml` 在项目根目录。

### 解决方案

**方法 1: 切换到项目根目录（推荐）**
```cmd
cd E:\projects\AIs\skill-creator
uv run dev
```

**方法 2: 使用启动脚本**
```cmd
# 双击运行或在任意目录执行
E:\projects\AIs\skill-creator\run_dev.cmd
```

**方法 3: 使用绝对路径**
```cmd
cd E:\projects\AIs\skill-creator
uv run dev
```

### 验证
```cmd
# 确认当前目录
cd

# 应该显示: E:\projects\AIs\skill-creator
# 而不是: E:\projects\AIs\skill-creator\backend
```

---

## 环境变量加载失败

### 症状 1: Field required 错误
```
pydantic_core._pydantic_core.ValidationError: 10 validation errors for Settings
SECRET_KEY
  Field required [type=missing, input_value={}, input_type=dict]
DATABASE_URL
  Field required [type=missing, input_value={}, input_type=dict]
...
```

### 原因
FastAPI 无法找到或读取 `.env` 文件。

### 解决方案

**步骤 1: 检查 .env 文件是否存在**
```cmd
cd E:\projects\AIs\skill-creator
dir .env
```

如果不存在：
```cmd
copy .env.example .env
```

**步骤 2: 手动复制到 backend 目录**
```cmd
copy .env backend\.env
```

**步骤 3: 验证内容**
```cmd
type .env
```

确保包含所有必需字段：
- SECRET_KEY
- DATABASE_URL
- MINIO_ENDPOINT
- MINIO_ACCESS_KEY
- MINIO_SECRET_KEY
- SSO_CLIENT_ID
- SSO_CLIENT_SECRET
- SSO_AUTHORIZE_URL
- SSO_TOKEN_URL
- SSO_USERINFO_URL

**步骤 4: 重新启动**
```cmd
uv run dev
```

---

### 症状 2: Extra inputs are not permitted (DEBUG)
```
pydantic_core._pydantic_core.ValidationError: 1 validation error for Settings
DEBUG
  Extra inputs are not permitted [type=extra_forbidden, input_value='true', input_type=str]
```

### 原因
`.env` 文件中有 `DEBUG=true`，但 Settings 类不接受这个字段。

### 解决方案

**已修复**: `backend/app/core/config.py` 中的 Settings 类已添加 `extra = "ignore"` 配置。

如果仍然出现此错误：

**方法 1: 更新 config.py（推荐）**
```python
class Settings(BaseSettings):
    # ... 其他字段 ...
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # 添加这一行
```

**方法 2: 从 .env 删除 DEBUG**
```cmd
# 编辑 .env 文件，删除或注释掉 DEBUG 行
# DEBUG=true  ← 删除这一行
```

---

## Docker 服务问题

### 症状 1: Docker 未安装
```
⚠️  Docker 未安装或 docker-compose 不可用
```

### 解决方案
1. 安装 Docker Desktop for Windows
2. 启动 Docker Desktop
3. 验证安装：
```cmd
docker --version
docker-compose --version
```

---

### 症状 2: Docker 服务启动失败
```
⚠️  Docker 启动失败: Command '['docker-compose', '-f', 'docker-compose.simple.yml', 'up', '-d']' returned non-zero exit status 1.
```

### 解决方案

**步骤 1: 检查 Docker Desktop 是否运行**
```cmd
docker ps
```

如果报错，启动 Docker Desktop。

**步骤 2: 手动启动服务**
```cmd
cd E:\projects\AIs\skill-creator
docker-compose -f docker-compose.simple.yml up -d
```

**步骤 3: 查看详细错误**
```cmd
docker-compose -f docker-compose.simple.yml logs
```

**步骤 4: 重置 Docker 服务**
```cmd
# 停止并删除容器
docker-compose -f docker-compose.simple.yml down

# 重新启动
docker-compose -f docker-compose.simple.yml up -d
```

---

### 症状 3: MinIO 端口被占用
```
Error: bind: address already in use (port 9000 or 9001)
```

### 解决方案

**查找占用进程**
```cmd
netstat -ano | findstr :9000
netstat -ano | findstr :9001
```

**停止占用进程**
```cmd
# 记下 PID（最后一列数字）
taskkill /PID <PID> /F
```

**或修改端口**

编辑 `docker-compose.simple.yml`:
```yaml
services:
  minio:
    ports:
      - "9010:9000"  # 改为 9010
      - "9011:9001"  # 改为 9011
```

同时修改 `.env`:
```env
MINIO_ENDPOINT=localhost:9010
```

---

## 数据库连接问题

### 症状: 无法连接到 MySQL
```
sqlalchemy.exc.OperationalError: (pymysql.err.OperationalError) (2003, "Can't connect to MySQL server on 'localhost'")
```

### 解决方案

**步骤 1: 检查 MySQL 是否运行**
```cmd
mysql -uroot -p -e "SELECT 1"
```

**步骤 2: 验证数据库存在**
```cmd
mysql -uroot -p -e "SHOW DATABASES LIKE 'skill_hub'"
```

如果不存在：
```cmd
mysql -uroot -p -e "CREATE DATABASE skill_hub CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
```

**步骤 3: 检查 .env 配置**
```env
# 确保用户名、密码、端口正确
DATABASE_URL=mysql+pymysql://root:你的密码@localhost:3306/skill_hub
```

**步骤 4: 测试连接**
```cmd
mysql -uroot -p你的密码 -e "USE skill_hub; SHOW TABLES;"
```

**步骤 5: 初始化数据库表**
```cmd
cd E:\projects\AIs\skill-creator
uv run db-init
```

---

## 端口冲突

### 8000 端口被占用

**查找进程**
```cmd
netstat -ano | findstr :8000
```

**停止进程**
```cmd
taskkill /PID <PID> /F
```

**或修改端口**

编辑 `skill_hub/cli.py`，修改 `--port` 参数：
```python
subprocess.run([
    sys.executable, "-m", "uvicorn",
    "app.main:app",
    "--reload",
    "--host", "0.0.0.0",
    "--port", "8001"  # 改为 8001
])
```

---

## 完整诊断流程

如果遇到问题，按以下顺序检查：

### 1. 检查运行目录
```cmd
cd
# 应该显示: E:\projects\AIs\skill-creator
```

### 2. 检查 .env 文件
```cmd
dir .env
type .env
```

### 3. 检查 Docker 服务
```cmd
docker ps
docker-compose -f docker-compose.simple.yml ps
```

### 4. 检查 MySQL 服务
```cmd
mysql -uroot -p -e "SELECT 1"
```

### 5. 检查端口占用
```cmd
netstat -ano | findstr :8000
netstat -ano | findstr :9000
netstat -ano | findstr :9001
netstat -ano | findstr :3306
```

### 6. 查看详细日志
```cmd
# Docker 日志
docker-compose -f docker-compose.simple.yml logs -f

# FastAPI 日志（启动服务后）
# 直接在终端查看输出
```

---

## 快速修复命令

```cmd
# 完整重置流程
cd E:\projects\AIs\skill-creator

# 1. 停止所有服务
docker-compose -f docker-compose.simple.yml down

# 2. 复制配置文件
copy .env backend\.env

# 3. 启动 Docker 服务
docker-compose -f docker-compose.simple.yml up -d

# 4. 等待服务启动
timeout /t 5

# 5. 启动开发服务器
uv run dev
```

---

## 仍然无法解决？

1. 检查 Python 版本: `python --version` (需要 3.11+)
2. 检查 uv 版本: `uv --version`
3. 重新安装依赖: `uv sync --reinstall`
4. 查看完整错误信息并搜索相关解决方案
5. 检查防火墙是否阻止端口访问

---

## 常用命令速查

```cmd
# 项目管理
cd E:\projects\AIs\skill-creator          # 切换到项目根目录
uv run dev                                 # 启动开发服务器
uv run db-init                             # 初始化数据库

# Docker 管理
docker-compose -f docker-compose.simple.yml up -d      # 启动服务
docker-compose -f docker-compose.simple.yml down       # 停止服务
docker-compose -f docker-compose.simple.yml ps         # 查看状态
docker-compose -f docker-compose.simple.yml logs -f    # 查看日志

# 数据库管理
mysql -uroot -p                            # 连接 MySQL
mysql -uroot -p skill_hub < create_tables.sql  # 导入 SQL

# 端口检查
netstat -ano | findstr :8000               # 检查 8000 端口
netstat -ano | findstr :9000               # 检查 9000 端口
taskkill /PID <PID> /F                     # 停止进程
```
