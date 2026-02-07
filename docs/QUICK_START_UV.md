# 使用 uv 快速启动指南

## ⚠️ 最重要的事

**所有命令必须在项目根目录运行！**

```cmd
# ✅ 正确
E:\projects\AIs\skill-creator> uv run dev

# ❌ 错误 - 不要在 backend 目录运行！
E:\projects\AIs\skill-creator\backend> uv run dev
```

---

## 🚀 最简单的启动方式

### 一次性设置（首次使用）

```bash
# 0. 确保在项目根目录
cd E:\projects\AIs\skill-creator

# 1. 创建虚拟环境
uv venv

# 2. 安装项目
uv pip install -e .

# 3. 配置环境变量
copy .env.example .env
```

**重要**: 编辑 `.env` 文件，修改 MySQL 密码：
```env
DATABASE_URL=mysql+pymysql://root:你的密码@localhost:3306/skill_hub
```

```bash
# 4. 初始化数据库
uv run db-init
```

选择 `1` 使用本地 MySQL，输入密码。

### 启动服务（每次开发）

```bash
# 确保在项目根目录！
cd E:\projects\AIs\skill-creator

# 启动服务
uv run dev
```

就这么简单！一条命令启动所有服务。

**记住**: 必须在 `E:\projects\AIs\skill-creator` 目录运行，不是 `backend` 目录！

## ✨ uv run dev 做了什么？

当你运行 `uv run dev` 时，它会自动：

1. ✅ **复制配置文件**
   - 自动复制 `.env` 到 `backend/.env`
   - 无需手动操作

2. ✅ **启动 Docker 服务**
   - 检查 MinIO 和 Redis 是否运行
   - 如果未运行，自动启动
   - 首次运行会下载镜像（约 2-3 分钟）

3. ✅ **启动开发服务器**
   - 启动 FastAPI 应用
   - 自动重载代码变更
   - 监听 0.0.0.0:8000

## 📝 完整流程示例

```bash
# 第一次使用
PS E:\projects\AIs\skill-creator> uv venv
PS E:\projects\AIs\skill-creator> uv pip install -e .
PS E:\projects\AIs\skill-creator> copy .env.example .env
# 编辑 .env 文件...
PS E:\projects\AIs\skill-creator> uv run db-init
选择数据库类型:
1. 本地 MySQL (localhost:3306)
2. Docker MySQL (localhost:3307)
请选择 (1/2, 默认 1): 1
请输入 MySQL root 密码: ****
✅ 数据库初始化完成！

# 启动服务
PS E:\projects\AIs\skill-creator> uv run dev
🚀 启动 Skill Hub 开发服务器...

📝 配置环境变量...
✅ .env 文件已复制到 backend 目录

📦 检查 Docker 服务...
🔄 启动 Docker 服务（MinIO + Redis）...
⏳ 等待服务启动...

📚 API 文档: http://localhost:8000/docs
🗄️  MinIO 控制台: http://localhost:9001 (minioadmin / minioadmin123)

按 Ctrl+C 停止服务器

INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

## 🌐 访问服务

启动成功后，访问：

- **API 文档**: http://localhost:8000/docs
- **API 根路径**: http://localhost:8000
- **MinIO 控制台**: http://localhost:9001
  - 用户名: `minioadmin`
  - 密码: `minioadmin123`

## 🔧 其他 uv 命令

```bash
# 初始化数据库
uv run db-init

# 重置数据库（删除所有数据）
uv run db-reset

# 运行测试
uv run pytest

# 格式化代码
uv run black backend/app

# 代码检查
uv run flake8 backend/app
```

## 💡 开发技巧

### 修改配置

1. 编辑根目录的 `.env` 文件
2. 重启服务（Ctrl+C 然后重新运行 `uv run dev`）
3. 配置会自动复制到 `backend/.env`

### 查看日志

```bash
# Docker 服务日志
docker logs skill-hub-minio
docker logs skill-hub-redis

# FastAPI 日志
# 直接在终端显示
```

### 停止服务

```bash
# 停止 FastAPI（在运行 uv run dev 的终端）
Ctrl+C

# 停止 Docker 服务
docker-compose -f docker-compose.simple.yml down
```

## 🐛 常见问题

### Q: 找不到 docker-compose.simple.yml 文件？

**错误信息**:
```
open E:\projects\AIs\skill-creator\backend\docker-compose.simple.yml: The system cannot find the file specified.
```

**原因**: 在 backend 目录运行命令，但文件在项目根目录。

**解决方法**:
```bash
# 切换到项目根目录
cd E:\projects\AIs\skill-creator

# 然后运行
uv run dev
```

### Q: 提示 "Field required" 错误？

A: `.env` 文件配置不完整。

**解决方法**:
```bash
# 检查 .env 文件是否存在
dir .env

# 如果不存在，复制模板
copy .env.example .env

# 编辑 .env，填写必需的配置
```

### Q: Docker 镜像下载很慢？

A: 首次运行需要下载 MinIO 和 Redis 镜像，请耐心等待。

**提示**: 可以配置 Docker 镜像加速器。

### Q: 端口被占用？

A: 检查端口占用情况：

```bash
# 检查 8000 端口
netstat -ano | findstr :8000

# 检查 9000 端口（MinIO）
netstat -ano | findstr :9000

# 检查 6379 端口（Redis）
netstat -ano | findstr :6379
```

**解决方法**: 修改端口或停止占用端口的程序。

### Q: MySQL 连接失败？

A: 检查 MySQL 服务和配置：

```bash
# 检查 MySQL 服务
net start | findstr MySQL

# 测试连接
mysql -u root -p -e "SHOW DATABASES;"

# 检查 .env 中的密码是否正确
```

## 📚 更多文档

- **uv 命令详解**: [UV_COMMANDS.md](UV_COMMANDS.md)
- **环境变量配置**: [ENV_FILE_GUIDE.md](ENV_FILE_GUIDE.md)
- **配置总结**: [CONFIGURATION_SUMMARY.md](CONFIGURATION_SUMMARY.md)
- **完整 README**: [README.md](README.md)

## 🎯 下一步

1. ✅ 访问 http://localhost:8000/docs 查看 API 文档
2. ✅ 尝试调用 API 接口
3. ✅ 修改代码，体验自动重载
4. ✅ 开始开发你的功能！

祝你开发愉快！🎉
