# MinIO 配置说明

## 当前配置

本项目使用**远程 MinIO 服务器**，无需在本地启动 MinIO 服务。

### 连接信息

```
服务器地址: 8.133.242.214:19000
访问密钥: root
秘密密钥: root10kv
使用 HTTPS: False
```

### 存储桶配置

- **默认存储桶**: `10kv-psychology`
- **SD 图片存储桶**: `sd-generated-images`

## 环境变量配置

在 `.env` 文件中配置：

```env
# MinIO 配置（远程服务器）
MINIO_ENDPOINT=8.133.242.214:19000
MINIO_ACCESS_KEY=root
MINIO_SECRET_KEY=root10kv
MINIO_SECURE=False
MINIO_USE_HTTPS=False

# MinIO 存储桶配置
DEFAULT_FILE_BUCKET=10kv-psychology
MINIO_BUCKET_NAME_SD=sd-generated-images
```

## 访问 MinIO 控制台

浏览器访问: http://8.133.242.214:19000

登录信息:
- 用户名: `root`
- 密码: `root10kv`

## 存储结构

### Skill Hub 使用的存储结构

```
10kv-psychology/  (默认存储桶)
├── project-name-1/  (项目桶)
│   ├── user_open_id_1/
│   │   ├── skill-1.md
│   │   ├── skill-2.md
│   │   └── my-project/
│   │       ├── docs/
│   │       │   └── README.md
│   │       └── src/
│   │           └── main.py
│   └── user_open_id_2/
│       └── skill-3.md
└── project-name-2/
    └── user_open_id_3/
        └── skill-4.md
```

## 使用示例

### Python 客户端连接

```python
from minio import Minio

# 创建 MinIO 客户端
client = Minio(
    "8.133.242.214:19000",
    access_key="root",
    secret_key="root10kv",
    secure=False
)

# 列出所有存储桶
buckets = client.list_buckets()
for bucket in buckets:
    print(bucket.name)

# 上传文件
client.fput_object(
    "10kv-psychology",
    "test/file.txt",
    "/path/to/local/file.txt"
)

# 下载文件
client.fget_object(
    "10kv-psychology",
    "test/file.txt",
    "/path/to/download/file.txt"
)
```

### 使用项目的 MinIO 服务

```python
from app.services.minio_service import minio_service

# 上传文件
result = minio_service.upload_file(
    bucket_name="10kv-psychology",
    object_name="user123/skill.md",
    file_data=file_stream,
    file_size=1024
)

# 下载文件
data = minio_service.download_file(
    bucket_name="10kv-psychology",
    object_name="user123/skill.md"
)

# 获取文件 URL
url = minio_service.get_file_url(
    bucket_name="10kv-psychology",
    object_name="user123/skill.md",
    expires=3600  # 1小时有效期
)
```

## 切换到本地 MinIO

如果需要使用本地 MinIO 进行开发，请按以下步骤操作：

### 1. 修改 docker-compose.yml

取消注释 MinIO 服务：

```yaml
  # MinIO 对象存储
  minio:
    image: minio/minio:latest
    container_name: skill-hub-minio
    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: minioadmin123
    ports:
      - "9000:9000"
      - "9001:9001"
    volumes:
      - minio_data:/data
    command: server /data --console-address ":9001"
    networks:
      - skill-hub-network
```

### 2. 修改 .env 文件

```env
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin123
MINIO_SECURE=False
MINIO_USE_HTTPS=False
DEFAULT_FILE_BUCKET=skill-hub
```

### 3. 启动服务

```bash
docker-compose up -d
```

### 4. 访问本地 MinIO

- 控制台: http://localhost:9001
- 用户名: minioadmin
- 密码: minioadmin123

## 安全建议

### 生产环境配置

在生产环境中，建议：

1. **启用 HTTPS**
```env
MINIO_SECURE=True
MINIO_USE_HTTPS=True
MINIO_ENDPOINT=minio.yourdomain.com:443
```

2. **使用强密码**
```env
MINIO_ACCESS_KEY=your-strong-access-key
MINIO_SECRET_KEY=your-very-strong-secret-key-min-32-chars
```

3. **配置存储桶策略**
```python
# 设置存储桶为私有
policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Deny",
            "Principal": {"AWS": ["*"]},
            "Action": ["s3:GetObject"],
            "Resource": ["arn:aws:s3:::bucket-name/*"]
        }
    ]
}
client.set_bucket_policy("bucket-name", json.dumps(policy))
```

4. **启用版本控制**
```python
client.set_bucket_versioning("bucket-name", VersioningConfig(ENABLED))
```

## 常见问题

### Q: 连接超时怎么办？
A: 检查网络连接和防火墙设置，确保可以访问 8.133.242.214:19000

### Q: 权限不足怎么办？
A: 确认 ACCESS_KEY 和 SECRET_KEY 是否正确，检查存储桶权限设置

### Q: 如何创建新的存储桶？
A: 
```python
from app.services.minio_service import minio_service
minio_service.ensure_bucket("new-bucket-name")
```

### Q: 如何查看存储使用情况？
A: 登录 MinIO 控制台查看，或使用 mc 命令行工具：
```bash
mc admin info myminio
```

## 监控和维护

### 查看存储使用情况

```bash
# 使用 mc 命令行工具
mc alias set myminio http://8.133.242.214:19000 root root10kv
mc du myminio/10kv-psychology
```

### 备份数据

```bash
# 备份整个存储桶
mc mirror myminio/10kv-psychology /backup/path/
```

### 清理过期文件

```python
from datetime import datetime, timedelta
from app.services.minio_service import minio_service

# 删除 30 天前的文件
cutoff_date = datetime.now() - timedelta(days=30)
# 实现清理逻辑
```

## 性能优化

1. **使用分片上传大文件**
2. **启用 CDN 加速**
3. **配置合适的过期策略**
4. **使用对象生命周期管理**

## 更多资源

- MinIO 官方文档: https://min.io/docs/
- MinIO Python SDK: https://min.io/docs/minio/linux/developers/python/minio-py.html
- MinIO 最佳实践: https://min.io/docs/minio/linux/operations/concepts.html
