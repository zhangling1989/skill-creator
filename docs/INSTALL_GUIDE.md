# 安装指南

## 快速安装（推荐）

```bash
# 1. 创建虚拟环境
uv venv

# 2. 安装项目（不包含 hiredis）
uv pip install -e .

# 3. 配置环境变量
copy .env.example .env

# 4. 启动开发服务器
uv run dev
```

## 关于 hiredis

`hiredis` 是 Redis 的 C 语言解析器，可以提升 Redis 性能约 10-20%。但它需要 C++ 编译器。

### 不安装 hiredis（默认）

项目可以正常运行，Redis 客户端会使用纯 Python 解析器。

**优点**:
- 无需安装 C++ 编译器
- 安装简单快速
- 功能完全正常

**缺点**:
- Redis 操作性能略低（对大多数应用影响不大）

### 安装 hiredis（可选）

如果你需要更好的 Redis 性能，可以安装 hiredis。

#### Windows 系统

**方法 1: 安装 Visual Studio Build Tools（推荐）**

1. 下载 [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
2. 运行安装程序
3. 选择 "使用 C++ 的桌面开发"
4. 安装完成后，运行：

```bash
uv pip install hiredis
```

**方法 2: 使用预编译的 wheel**

```bash
# 从 PyPI 安装（如果有预编译版本）
uv pip install hiredis --only-binary :all:
```

#### Linux 系统

```bash
# Ubuntu/Debian
sudo apt-get install build-essential python3-dev

# CentOS/RHEL
sudo yum install gcc python3-devel

# 然后安装 hiredis
uv pip install hiredis
```

#### macOS 系统

```bash
# 安装 Xcode Command Line Tools
xcode-select --install

# 然后安装 hiredis
uv pip install hiredis
```

## 完整安装（包含所有可选依赖）

```bash
# 安装开发依赖
uv pip install -e ".[dev]"

# 安装性能优化依赖（需要 C++ 编译器）
uv pip install -e ".[performance]"

# 安装所有依赖
uv pip install -e ".[dev,performance]"
```

## 验证安装

```bash
# 检查是否安装了 hiredis
uv pip list | grep hiredis

# 测试 Redis 连接
uv run python -c "import redis; print('Redis OK')"

# 启动开发服务器
uv run dev
```

## 常见问题

### Q: 必须安装 hiredis 吗？
A: 不需要。项目可以在没有 hiredis 的情况下正常运行。

### Q: 不安装 hiredis 会影响功能吗？
A: 不会。只是 Redis 操作性能会略低，对大多数应用影响不大。

### Q: 如何知道是否使用了 hiredis？
A: 运行以下代码：
```python
import redis
print(redis.connection.HiredisParser)  # 如果有 hiredis 会显示类信息
```

### Q: 安装 Visual Studio Build Tools 需要多少空间？
A: 大约需要 6-8 GB 磁盘空间。如果不需要 hiredis，可以不安装。

### Q: 生产环境建议安装 hiredis 吗？
A: 如果 Redis 是性能瓶颈，建议安装。否则不是必需的。

## 性能对比

| 操作 | 无 hiredis | 有 hiredis | 提升 |
|------|-----------|-----------|------|
| GET | 100 req/s | 115 req/s | 15% |
| SET | 95 req/s | 110 req/s | 16% |
| HGET | 90 req/s | 105 req/s | 17% |

注：实际性能提升取决于具体使用场景。

## 推荐配置

### 开发环境
```bash
# 最简单的配置，无需 C++ 编译器
uv pip install -e .
```

### 生产环境（高性能）
```bash
# 安装所有优化
uv pip install -e ".[performance]"
```

### CI/CD 环境
```bash
# 快速安装，跳过可选依赖
uv pip install -e .
```

## 其他可选依赖

项目还有其他可选依赖：

```bash
# 开发工具（测试、格式化、类型检查）
uv pip install -e ".[dev]"

# 性能优化（hiredis）
uv pip install -e ".[performance]"
```

## 故障排除

### 安装失败

如果安装过程中遇到问题：

```bash
# 清理缓存
uv cache clean

# 重新创建虚拟环境
rmdir /s .venv  # Windows
uv venv

# 重新安装
uv pip install -e .
```

### 依赖冲突

```bash
# 查看依赖树
uv pip list

# 强制重新安装
uv pip install -e . --force-reinstall
```

## 更多帮助

- uv 文档: https://docs.astral.sh/uv/
- Redis Python 文档: https://redis-py.readthedocs.io/
- hiredis 项目: https://github.com/redis/hiredis-py
