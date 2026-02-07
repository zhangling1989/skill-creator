# 环境变量配置指南

## 问题说明

FastAPI 应用在 `backend` 目录下运行，需要在该目录下有 `.env` 文件才能读取配置。

## 解决方案

### 自动方式（推荐）

使用 `start_local.cmd` 脚本会自动复制 `.env` 文件到 `backend` 目录：

```cmd
start_local.cmd
```

### 手动方式

如果需要手动复制：

```cmd
# Windows CMD
copy .env backend\.env

# Windows PowerShell
Copy-Item .env backend\.env
```

## 文件结构

```
skill-creator/
├── .env                    # 主配置文件（编辑这个）
├── .env.example           # 配置模板
├── backend/
│   ├── .env              # 自动复制的配置（不要直接编辑）
│   └── app/
│       └── main.py
└── ...
```

## 配置管理

### 修改配置

1. **编辑根目录的 `.env` 文件**
   ```env
   DATABASE_URL=mysql+pymysql://root:你的密码@localhost:3306/skill_hub
   MINIO_ENDPOINT=localhost:9000
   ...
   ```

2. **重新复制到 backend 目录**
   ```cmd
   copy .env backend\.env
   ```

3. **重启服务**
   ```cmd
   # 按 Ctrl+C 停止服务
   # 然后重新运行
   start_local.cmd
   ```

### 为什么需要两个 .env 文件？

- **根目录 `.env`**: 主配置文件，方便管理和版本控制
- **backend/.env`**: FastAPI 运行时读取的文件

## 环境变量说明

### 必需配置

```env
# 数据库（必需）
DATABASE_URL=mysql+pymysql://root:root@localhost:3306/skill_hub

# MinIO（必需）
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin123

# 应用密钥（必需）
SECRET_KEY=your-secret-key-change-in-production-min-32-chars

# SSO 配置（必需，但可以使用示例值）
SSO_CLIENT_ID=your_client_id
SSO_CLIENT_SECRET=your_client_secret
SSO_AUTHORIZE_URL=https://sso.example.com/oauth/authorize
SSO_TOKEN_URL=https://sso.example.com/oauth/token
SSO_USERINFO_URL=https://sso.example.com/oauth/userinfo
```

### 可选配置

```env
# MinIO 存储桶
DEFAULT_FILE_BUCKET=skill-hub
MINIO_BUCKET_NAME_SD=sd-generated-images

# Redis
REDIS_URL=redis://localhost:6379/0

# 调试模式
DEBUG=true

# CORS
ALLOWED_ORIGINS=["http://localhost:3000","http://localhost:8000"]
```

## 常见问题

### Q: 为什么启动时报错 "Field required"？

A: 因为 `backend/.env` 文件不存在或配置不完整。

**解决方法**:
```cmd
copy .env backend\.env
```

### Q: 修改了 .env 但没有生效？

A: 需要重新复制到 backend 目录并重启服务。

**解决方法**:
```cmd
copy .env backend\.env
# 重启服务
```

### Q: 可以直接编辑 backend/.env 吗？

A: 不推荐。因为这个文件是自动生成的，可能会被覆盖。应该编辑根目录的 `.env`。

### Q: 如何在不同环境使用不同配置？

A: 创建多个配置文件：

```cmd
# 开发环境
.env.development

# 生产环境
.env.production

# 使用时复制对应的文件
copy .env.development .env
copy .env backend\.env
```

## 安全建议

1. **不要提交 .env 文件到 Git**
   - `.gitignore` 已配置忽略 `.env` 文件
   - 只提交 `.env.example` 作为模板

2. **使用强密码**
   ```env
   SECRET_KEY=使用至少32个字符的随机字符串
   MINIO_SECRET_KEY=使用强密码
   ```

3. **生产环境配置**
   ```env
   DEBUG=false
   MINIO_SECURE=True
   MINIO_USE_HTTPS=True
   ```

## 自动化脚本

### 更新配置脚本

创建 `update_env.cmd`:

```cmd
@echo off
echo 更新 backend 环境变量...
copy .env backend\.env
echo 完成！
pause
```

### 检查配置脚本

创建 `check_env.cmd`:

```cmd
@echo off
echo 检查环境变量配置...
echo.

if exist ".env" (
    echo ✓ 根目录 .env 存在
) else (
    echo ✗ 根目录 .env 不存在
)

if exist "backend\.env" (
    echo ✓ backend\.env 存在
) else (
    echo ✗ backend\.env 不存在
    echo.
    echo 运行以下命令创建:
    echo copy .env backend\.env
)

echo.
pause
```

## 配置模板

完整的 `.env` 模板：

```env
# 数据库配置（使用本地 MySQL）
DATABASE_URL=mysql+pymysql://root:root@localhost:3306/skill_hub

# MinIO 配置（本地 Docker）
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin123
MINIO_SECURE=False
MINIO_USE_HTTPS=False

# MinIO 存储桶配置
DEFAULT_FILE_BUCKET=skill-hub
MINIO_BUCKET_NAME_SD=sd-generated-images

# SSO 配置
SSO_CLIENT_ID=your_client_id
SSO_CLIENT_SECRET=your_client_secret
SSO_AUTHORIZE_URL=https://sso.example.com/oauth/authorize
SSO_TOKEN_URL=https://sso.example.com/oauth/token
SSO_USERINFO_URL=https://sso.example.com/oauth/userinfo
SSO_REDIRECT_URI=http://localhost:8000/api/v1/auth/callback

# Redis 配置
REDIS_URL=redis://localhost:6379/0

# 应用配置
SECRET_KEY=your-secret-key-change-in-production-min-32-chars
DEBUG=true

# CORS 配置
ALLOWED_ORIGINS=["http://localhost:3000","http://localhost:8000"]
```

## 验证配置

启动服务后，如果看到以下输出说明配置正确：

```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

如果看到 "Field required" 错误，说明配置文件有问题。
