# 配置总结

## 当前配置

### 数据库
- **类型**: MySQL
- **位置**: 本地（localhost:3306）
- **数据库名**: skill_hub
- **用户**: root
- **说明**: 使用你本地已安装的 MySQL

### MinIO 对象存储
- **类型**: MinIO
- **位置**: 本地 Docker（localhost:9000）
- **控制台**: http://localhost:9001
- **用户名**: minioadmin
- **密码**: minioadmin123
- **默认存储桶**: skill-hub
- **说明**: 通过 Docker 运行，数据持久化在 Docker volume

### Redis 缓存
- **类型**: Redis
- **位置**: 本地 Docker（localhost:6379）
- **说明**: 通过 Docker 运行

## 服务架构

```
┌─────────────────────────────────────────┐
│         Skill Hub 应用                   │
│      (FastAPI - Port 8000)              │
└─────────────────────────────────────────┘
           │         │         │
           ▼         ▼         ▼
    ┌──────────┐ ┌──────────┐ ┌──────────┐
    │  MySQL   │ │  MinIO   │ │  Redis   │
    │  (本地)  │ │ (Docker) │ │ (Docker) │
    │  :3306   │ │  :9000   │ │  :6379   │
    └──────────┘ └──────────┘ └──────────┘
```

## 端口使用

| 服务 | 端口 | 说明 |
|------|------|------|
| FastAPI | 8000 | API 服务 |
| MySQL | 3306 | 数据库（本地） |
| MinIO API | 9000 | 对象存储 API |
| MinIO Console | 9001 | MinIO 管理控制台 |
| Redis | 6379 | 缓存服务 |

## 环境变量 (.env)

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

# SSO 配置（需要配置实际的 SSO 服务）
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

## Docker 服务

### 使用 docker-compose.simple.yml（推荐）

只启动 MinIO 和 Redis，使用本地 MySQL：

```cmd
docker-compose -f docker-compose.simple.yml up -d
```

包含的服务：
- ✅ MinIO (9000, 9001)
- ✅ Redis (6379)
- ❌ MySQL（使用本地）

### 使用 docker-compose.yml（完整）

启动所有服务（包括 Docker MySQL）：

```cmd
docker-compose up -d
```

包含的服务：
- ✅ MySQL (3307) - 注意端口改为 3307
- ✅ MinIO (9000, 9001)
- ✅ Redis (6379)
- ✅ Backend (8000)

## 启动流程

### 方式 1: 使用脚本（推荐）

```cmd
# 1. 初始化数据库
init_local_db.cmd

# 2. 启动服务
start_local.cmd
```

### 方式 2: 手动启动

```cmd
# 1. 启动 Docker 服务
docker-compose -f docker-compose.simple.yml up -d

# 2. 初始化数据库（首次）
mysql -u root -p skill_hub < create_tables.sql

# 3. 启动开发服务器
cd backend
uv run uvicorn app.main:app --reload
```

### 方式 3: 使用 uv 命令

```cmd
# 1. 启动 Docker 服务
docker-compose -f docker-compose.simple.yml up -d

# 2. 初始化数据库（首次）
uv run db-init

# 3. 启动开发服务器
uv run dev
```

## 数据持久化

### MySQL
- **位置**: 本地 MySQL 数据目录
- **备份**: 使用 mysqldump

### MinIO
- **位置**: Docker volume `skill-creator_minio_data`
- **查看**: `docker volume inspect skill-creator_minio_data`
- **备份**: `docker run --rm -v skill-creator_minio_data:/data -v $(pwd):/backup alpine tar czf /backup/minio-backup.tar.gz /data`

### Redis
- **位置**: Docker volume `skill-creator_redis_data`
- **持久化**: RDB 快照

## 访问地址

- **API 文档**: http://localhost:8000/docs
- **API 根路径**: http://localhost:8000
- **MinIO 控制台**: http://localhost:9001
  - 用户名: minioadmin
  - 密码: minioadmin123

## 常见操作

### 查看 Docker 服务状态
```cmd
docker-compose -f docker-compose.simple.yml ps
```

### 查看日志
```cmd
# MinIO 日志
docker logs skill-hub-minio

# Redis 日志
docker logs skill-hub-redis
```

### 停止服务
```cmd
# 停止 Docker 服务
docker-compose -f docker-compose.simple.yml down

# 停止并删除数据
docker-compose -f docker-compose.simple.yml down -v
```

### 重启服务
```cmd
docker-compose -f docker-compose.simple.yml restart
```

## 故障排除

### MinIO 无法访问

1. 检查容器状态：
   ```cmd
   docker ps | findstr minio
   ```

2. 查看日志：
   ```cmd
   docker logs skill-hub-minio
   ```

3. 重启服务：
   ```cmd
   docker-compose -f docker-compose.simple.yml restart minio
   ```

### MySQL 连接失败

1. 检查 MySQL 服务：
   ```cmd
   net start | findstr MySQL
   ```

2. 测试连接：
   ```cmd
   mysql -u root -p -e "SHOW DATABASES;"
   ```

3. 检查 .env 配置中的密码是否正确

### Redis 连接失败

1. 检查容器状态：
   ```cmd
   docker ps | findstr redis
   ```

2. 测试连接：
   ```cmd
   docker exec -it skill-hub-redis redis-cli ping
   ```

## 开发建议

1. **使用本地 MySQL**: 更快，更方便调试
2. **使用 Docker MinIO**: 隔离环境，易于重置
3. **使用 Docker Redis**: 轻量级，易于管理
4. **定期备份**: 特别是 MinIO 数据

## 生产环境配置

生产环境建议：

1. **使用独立的 MySQL 服务器**
2. **使用独立的 MinIO 集群**
3. **使用 Redis 集群**
4. **启用 HTTPS**
5. **配置防火墙规则**
6. **设置强密码**
7. **配置备份策略**
