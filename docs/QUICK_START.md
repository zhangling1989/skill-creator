# 快速启动指南

## ✅ 安装成功！

恭喜！项目依赖已经安装完成。

## 🚀 启动服务

### 使用 uv 命令（最简单）

```bash
# 启动开发服务器（自动启动 Docker 并运行服务）
uv run dev
```

就这么简单！

### 首次启动说明

首次运行时，Docker 会下载 MySQL 和 Redis 镜像，可能需要几分钟。请耐心等待。

下载完成后，你会看到：

```
🚀 启动 Skill Hub 开发服务器...
📦 检查 Docker 服务...
✅ Docker 服务已运行

📚 API 文档: http://localhost:8000/docs
🗄️  远程 MinIO: http://8.133.242.214:19000

按 Ctrl+C 停止服务器

INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

## 📝 配置环境变量

在首次启动前，建议配置环境变量：

```bash
# 复制配置模板
copy .env.example .env

# 编辑 .env 文件（可选，使用默认配置也可以）
```

## 🗄️ 初始化数据库

等 Docker 服务启动完成后（约 15-30 秒），初始化数据库：

```bash
# 方式 1: 使用 uv 命令
uv run db-init

# 方式 2: 手动执行
type create_tables.sql | docker exec -i skill-hub-mysql mysql -uroot -proot123 skill_hub
```

## 🌐 访问服务

启动成功后，访问：

- **API 文档**: http://localhost:8000/docs
- **API 根路径**: http://localhost:8000
- **远程 MinIO**: http://8.133.242.214:19000
  - 用户名: `root`
  - 密码: `root10kv`

## 📋 常用命令

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

## 🐛 故障排除

### Docker 下载慢？

如果 Docker 镜像下载很慢，可以配置国内镜像源。

### 端口被占用？

如果 8000 端口被占用，修改启动命令：

```bash
cd backend
uv run uvicorn app.main:app --reload --port 8001
```

### 数据库连接失败？

确保 Docker 服务已启动：

```bash
docker-compose ps
```

如果服务未运行：

```bash
docker-compose up -d
```

## 📚 更多文档

- **完整安装指南**: [INSTALL_GUIDE.md](INSTALL_GUIDE.md)
- **uv 命令详解**: [UV_COMMANDS.md](UV_COMMANDS.md)
- **PowerShell 问题**: [POWERSHELL_FIX.md](POWERSHELL_FIX.md)
- **MinIO 配置**: [docs/minio_configuration.md](docs/minio_configuration.md)

## 🎉 开始开发

现在你可以开始开发了！

1. 访问 http://localhost:8000/docs 查看 API 文档
2. 修改 `backend/app` 目录下的代码
3. 服务器会自动重载，无需手动重启

祝你开发愉快！🚀
