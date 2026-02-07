# 端口冲突解决方案

## 问题

你的本地 3306 端口已被占用（本地 MySQL 正在运行），导致 Docker MySQL 无法启动。

## 解决方案

### 方案 1: 使用本地 MySQL（推荐）

既然你本地已经有 MySQL 了，直接使用它！

#### 步骤：

1. **初始化数据库**
   ```cmd
   init_local_db.cmd
   ```
   输入你的 MySQL root 密码，脚本会自动创建数据库和表。

2. **启动服务**（只启动 Redis）
   ```cmd
   start_local.cmd
   ```

3. **访问服务**
   - API 文档: http://localhost:8000/docs

### 方案 2: 修改 Docker MySQL 端口

如果你想同时使用 Docker MySQL 和本地 MySQL：

1. **修改 .env 文件**
   ```env
   DATABASE_URL=mysql+pymysql://skillhub:skillhub123@localhost:3307/skill_hub
   ```

2. **停止现有容器**
   ```cmd
   docker-compose down
   ```

3. **启动服务**（Docker MySQL 会使用 3307 端口）
   ```cmd
   docker-compose up -d
   ```

4. **初始化数据库**
   ```cmd
   type create_tables.sql | docker exec -i skill-hub-mysql mysql -uroot -proot123 skill_hub
   ```

### 方案 3: 停止本地 MySQL

如果你不需要本地 MySQL：

1. **停止本地 MySQL 服务**
   ```cmd
   # Windows 服务管理
   net stop MySQL80
   
   # 或在服务管理器中停止 MySQL 服务
   ```

2. **启动 Docker 服务**
   ```cmd
   docker-compose up -d
   ```

## 当前配置

### 使用本地 MySQL

`.env` 文件配置：
```env
DATABASE_URL=mysql+pymysql://root:root@localhost:3306/skill_hub
```

启动命令：
```cmd
start_local.cmd
```

### 使用 Docker MySQL（3307 端口）

`.env` 文件配置：
```env
DATABASE_URL=mysql+pymysql://skillhub:skillhub123@localhost:3307/skill_hub
```

启动命令：
```cmd
docker-compose up -d
uv run dev
```

## 验证配置

### 检查本地 MySQL

```cmd
# 查看 MySQL 是否运行
netstat -ano | findstr :3306

# 连接测试
mysql -u root -p -e "SHOW DATABASES;"
```

### 检查 Docker 服务

```cmd
# 查看运行的容器
docker ps

# 查看日志
docker-compose logs mysql
```

## 推荐配置

**对于开发环境，推荐使用方案 1（本地 MySQL）**：

优点：
- ✅ 无需下载 Docker MySQL 镜像
- ✅ 启动更快
- ✅ 可以使用熟悉的 MySQL 工具
- ✅ 节省资源

步骤：
```cmd
# 1. 初始化数据库
init_local_db.cmd

# 2. 启动服务
start_local.cmd
```

就这么简单！
