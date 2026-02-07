# 🚀 Skill Hub 快速启动指南

## ⚠️ 重要提示

**必须从项目根目录运行所有命令！**

```cmd
# 正确 ✅
E:\projects\AIs\skill-creator> uv run dev

# 错误 ❌
E:\projects\AIs\skill-creator\backend> uv run dev
```

---

## 📋 前置要求

1. **Python 3.11+** - 已安装 ✅
2. **uv** - Python 包管理工具 ✅
3. **MySQL** - 本地运行在 3306 端口 ✅
4. **Docker Desktop** - 用于运行 MinIO 和 Redis

---

## 🎯 快速启动（3步）

### 1️⃣ 确保在项目根目录

```cmd
cd E:\projects\AIs\skill-creator
```

### 2️⃣ 启动 Docker 服务

```cmd
docker-compose -f docker-compose.simple.yml up -d
```

这会启动：
- MinIO (对象存储) - http://localhost:9001
- Redis (缓存) - localhost:6379

### 3️⃣ 启动开发服务器

```cmd
uv run dev
```

服务启动后访问：
- **API 文档**: http://localhost:8000/docs
- **MinIO 控制台**: http://localhost:9001 (minioadmin / minioadmin123)

---

## 🗄️ 数据库初始化

首次运行需要初始化数据库：

```cmd
# 确保在项目根目录
cd E:\projects\AIs\skill-creator

# 初始化数据库表
uv run db-init
```

选择 `1` (本地 MySQL)，输入你的 MySQL root 密码。

---

## 🛠️ 常用命令

所有命令都必须在项目根目录 `E:\projects\AIs\skill-creator` 运行：

```cmd
# 启动开发服务器（自动重载）
uv run dev

# 启动生产服务器
uv run start

# 初始化数据库
uv run db-init

# 重置数据库（删除所有数据）
uv run db-reset

# 查看 Docker 服务状态
docker-compose -f docker-compose.simple.yml ps

# 停止 Docker 服务
docker-compose -f docker-compose.simple.yml down

# 查看 Docker 日志
docker-compose -f docker-compose.simple.yml logs -f
```

---

## ❌ 常见错误

### 错误 1: 找不到 docker-compose.simple.yml

**原因**: 在错误的目录运行命令

**解决**:
```cmd
cd E:\projects\AIs\skill-creator
uv run dev
```

### 错误 2: ValidationError - Field required

**原因**: .env 文件未正确加载

**解决**:
```cmd
# 确保 .env 文件存在
dir .env

# 手动复制到 backend 目录
copy .env backend\.env

# 然后启动
uv run dev
```

### 错误 3: Extra inputs are not permitted (DEBUG)

**原因**: .env 中有 Settings 类不需要的字段

**解决**: 已修复，Settings 类配置了 `extra = "ignore"`

### 错误 4: 端口被占用

**MinIO 端口冲突**:
```cmd
# 查看占用 9000 端口的进程
netstat -ano | findstr :9000

# 停止 Docker 服务
docker-compose -f docker-compose.simple.yml down
```

**MySQL 端口冲突**:
- 项目使用本地 MySQL (3306)，不会冲突
- Docker MySQL 已改为 3307 端口

---

## 📁 项目结构

```
E:\projects\AIs\skill-creator\          ← 必须在这里运行命令！
├── .env                                 ← 主配置文件
├── docker-compose.simple.yml            ← Docker 服务配置
├── pyproject.toml                       ← uv 项目配置
├── skill_hub/                           ← CLI 工具
│   └── cli.py                           ← dev, start, db-init 命令
└── backend/                             ← FastAPI 应用
    ├── .env                             ← 自动从根目录复制
    └── app/
        ├── main.py                      ← FastAPI 入口
        ├── core/
        │   └── config.py                ← 配置加载
        ├── api/
        ├── models/
        └── services/
```

---

## 🔧 配置说明

### .env 文件配置

```env
# 数据库 - 使用本地 MySQL
DATABASE_URL=mysql+pymysql://root:root@localhost:3306/skill_hub

# MinIO - 本地 Docker 服务
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin123

# 其他配置保持默认即可
```

### 修改 MySQL 密码

如果你的 MySQL root 密码不是 `root`，修改 `.env`:

```env
DATABASE_URL=mysql+pymysql://root:你的密码@localhost:3306/skill_hub
```

---

## 🎉 验证安装

1. **检查 Docker 服务**:
```cmd
docker-compose -f docker-compose.simple.yml ps
```

应该看到 MinIO 和 Redis 都是 `Up` 状态。

2. **访问 API 文档**:
打开浏览器访问 http://localhost:8000/docs

3. **访问 MinIO 控制台**:
打开浏览器访问 http://localhost:9001
- 用户名: minioadmin
- 密码: minioadmin123

---

## 📞 需要帮助？

如果遇到问题：

1. 确认在项目根目录: `cd E:\projects\AIs\skill-creator`
2. 检查 Docker 是否运行: `docker ps`
3. 检查 MySQL 是否运行: `mysql -uroot -p -e "SELECT 1"`
4. 查看详细日志: `docker-compose -f docker-compose.simple.yml logs -f`

---

## 🚀 下一步

服务启动成功后，你可以：

1. 访问 API 文档测试接口: http://localhost:8000/docs
2. 上传 Skill 文件
3. 管理分类和项目
4. 查看 MinIO 中的文件存储

祝你使用愉快！🎊
