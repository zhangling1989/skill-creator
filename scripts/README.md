# 🔧 Skill Hub 脚本目录

本目录包含 Skill Hub 项目的所有脚本文件。

## 📋 脚本列表

### 启动脚本

#### Windows CMD 脚本

- **`run_dev.cmd`** - 一键启动开发服务器（推荐）
  ```cmd
  scripts\run_dev.cmd
  ```
  自动处理：切换目录、复制配置、启动 Docker、启动服务器

- **`start_dev.cmd`** - 启动开发服务器
  ```cmd
  scripts\start_dev.cmd
  ```

- **`start_local.cmd`** - 使用本地 MySQL 启动
  ```cmd
  scripts\start_local.cmd
  ```

#### PowerShell 脚本

- **`start_dev.ps1`** - PowerShell 版启动脚本
  ```powershell
  .\scripts\start_dev.ps1
  ```

- **`tasks.ps1`** - 任务管理脚本
  ```powershell
  .\scripts\tasks.ps1
  ```

### 安装脚本

- **`setup.cmd`** - Windows CMD 安装脚本
  ```cmd
  scripts\setup.cmd
  ```

- **`setup.ps1`** - PowerShell 安装脚本
  ```powershell
  .\scripts\setup.ps1
  ```

### 数据库脚本

- **`init_local_db.cmd`** - 初始化本地数据库
  ```cmd
  scripts\init_local_db.cmd
  ```

---

## 🚀 快速使用

### 首次安装

```cmd
# 1. 运行安装脚本
scripts\setup.cmd

# 2. 初始化数据库
scripts\init_local_db.cmd

# 3. 启动服务
scripts\run_dev.cmd
```

### 日常开发

```cmd
# 直接启动（推荐）
scripts\run_dev.cmd

# 或者使用 uv 命令（需要在项目根目录）
cd E:\projects\AIs\skill-creator
uv run dev
```

---

## 📝 脚本说明

### run_dev.cmd（推荐使用）

这是最方便的启动脚本，它会：

1. ✅ 自动切换到项目根目录
2. ✅ 检查并复制 .env 文件
3. ✅ 启动 Docker 服务（MinIO + Redis）
4. ✅ 启动 FastAPI 开发服务器
5. ✅ 显示服务地址和访问信息

**特点**：
- 可以在任何目录运行
- 自动处理所有依赖
- 友好的中文提示

### start_dev.cmd vs start_local.cmd

- **start_dev.cmd**: 标准开发启动，使用 Docker MySQL
- **start_local.cmd**: 使用本地 MySQL（端口 3306）

### PowerShell 脚本注意事项

如果遇到 "禁止运行脚本" 错误：

```powershell
# 方法 1: 临时允许
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# 方法 2: 使用 CMD 脚本代替
scripts\run_dev.cmd
```

---

## 🔧 自定义脚本

你可以复制并修改这些脚本来适应你的需求：

```cmd
# 复制模板
copy scripts\run_dev.cmd scripts\my_custom_start.cmd

# 编辑自定义脚本
notepad scripts\my_custom_start.cmd
```

---

## 📚 相关文档

- **快速启动**: 查看 `../docs/现在就开始.md`
- **故障排除**: 查看 `../docs/TROUBLESHOOTING.md`
- **环境配置**: 查看 `../docs/ENV_FILE_GUIDE.md`

---

## 💡 提示

1. **推荐使用 `run_dev.cmd`** - 最简单、最可靠
2. **遇到问题先查看文档** - `docs/TROUBLESHOOTING.md`
3. **可以从任何位置运行** - 脚本会自动切换到正确目录
