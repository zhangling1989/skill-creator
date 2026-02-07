# 🎉 最终使用指南

## ✅ 所有问题已解决

项目现在可以完美运行了！

## 🚀 快速启动（推荐方式）

### 在项目根目录运行

```bash
# 确保在项目根目录
cd E:\projects\AIs\skill-creator

# 启动服务
uv run dev
```

**重要**: 必须在项目根目录运行，不要在 backend 目录运行！

## 📝 完整流程

### 首次使用

```bash
# 1. 进入项目目录
cd E:\projects\AIs\skill-creator

# 2. 创建虚拟环境
uv venv

# 3. 安装依赖
uv pip install -e .

# 4. 配置环境变量
copy .env.example .env
# 编辑 .env，修改 MySQL 密码

# 5. 初始化数据库
uv run db-init
# 选择 1（本地 MySQL），输入密码

# 6. 启动服务
uv run dev
```

### 每次开发

```bash
# 进入项目根目录
cd E:\projects\AIs\skill-creator

# 启动服务
uv run dev
```

## ✨ uv run dev 做了什么

1. ✅ 自动复制 `.env` 到 `backend/.env`
2. ✅ 检查并启动 Docker 服务（MinIO + Redis）
3. ✅ 启动 FastAPI 开发服务器
4. ✅ 自动重载代码变更

## 🌐 访问地址

启动成功后，你会看到：

```
🚀 启动 Skill Hub 开发服务器...

📝 配置环境变量...
✅ .env 文件已复制到 backend 目录

📦 检查 Docker 服务...
✅ Docker 服务已运行

📚 API 文档: http://localhost:8000/docs
🗄️  MinIO 控制台: http://localhost:9001 (minioadmin / minioadmin123)

按 Ctrl+C 停止服务器

INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

访问：
- **API 文档**: http://localhost:8000/docs
- **MinIO 控制台**: http://localhost:9001

## 🔧 其他命令

```bash
# 初始化数据库
uv run db-init

# 重置数据库
uv run db-reset

# 运行测试
uv run pytest

# 格式化代码
uv run black backend/app
```

## ⚠️ 常见错误

### 错误 1: 在 backend 目录运行

```bash
# ❌ 错误
PS E:\projects\AIs\skill-creator\backend> uv run dev

# ✅ 正确
PS E:\projects\AIs\skill-creator> uv run dev
```

### 错误 2: .env 文件不存在

```bash
# 创建 .env 文件
copy .env.example .env
```

### 错误 3: DEBUG 字段错误

已修复！配置文件现在会忽略 .env 中的额外字段。

### 错误 4: Docker 服务未启动

```bash
# 手动启动
docker-compose -f docker-compose.simple.yml up -d
```

## 📂 项目结构

```
E:\projects\AIs\skill-creator\     ← 在这里运行 uv run dev
├── .env                           ← 主配置文件
├── backend/
│   ├── .env                       ← 自动复制的配置
│   └── app/
│       └── main.py
├── docker-compose.simple.yml      ← Docker 配置
├── skill_hub/
│   └── cli.py                     ← uv 命令实现
└── pyproject.toml                 ← 项目配置
```

## 🎯 开发工作流

### 1. 启动服务

```bash
cd E:\projects\AIs\skill-creator
uv run dev
```

### 2. 修改代码

编辑 `backend/app/` 下的文件，服务器会自动重载。

### 3. 测试 API

访问 http://localhost:8000/docs 测试接口。

### 4. 停止服务

在运行 `uv run dev` 的终端按 `Ctrl+C`。

### 5. 停止 Docker（可选）

```bash
docker-compose -f docker-compose.simple.yml down
```

## 💡 提示

1. **始终在项目根目录运行命令**
2. **修改配置后重启服务**
3. **使用 API 文档测试接口**
4. **查看终端日志排查问题**

## 📚 相关文档

- **uv 快速启动**: [QUICK_START_UV.md](QUICK_START_UV.md)
- **uv 命令详解**: [UV_COMMANDS.md](UV_COMMANDS.md)
- **环境变量配置**: [ENV_FILE_GUIDE.md](ENV_FILE_GUIDE.md)
- **配置总结**: [CONFIGURATION_SUMMARY.md](CONFIGURATION_SUMMARY.md)

## 🎉 开始开发

现在一切就绪，开始你的开发之旅吧！

```bash
cd E:\projects\AIs\skill-creator
uv run dev
```

祝你开发愉快！🚀
