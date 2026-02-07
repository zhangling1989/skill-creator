# PowerShell 执行策略问题解决方案

## 问题描述

在 Windows 上运行 PowerShell 脚本时出现错误：
```
无法加载文件，因为在此系统上禁止运行脚本
```

## 解决方案

### 方案 1：使用 CMD 脚本（推荐，最简单）

我已经创建了 CMD 版本的脚本，可以直接使用：

```cmd
# 设置项目
setup.cmd

# 启动开发服务器
start_dev.cmd
```

### 方案 2：临时允许执行（当前会话）

在 PowerShell 中运行：

```powershell
# 以管理员身份打开 PowerShell，然后执行：
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process

# 然后运行脚本
.\start_dev.ps1
```

### 方案 3：为当前用户永久允许（推荐）

```powershell
# 以管理员身份打开 PowerShell，然后执行：
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 然后就可以正常运行脚本了
.\start_dev.ps1
```

### 方案 4：绕过执行策略运行单个脚本

```powershell
# 不需要管理员权限
powershell -ExecutionPolicy Bypass -File .\start_dev.ps1
```

### 方案 5：手动执行命令（最安全）

如果不想修改执行策略，可以手动执行以下命令：

```powershell
# 1. 激活虚拟环境
.venv\Scripts\Activate.ps1

# 2. 启动 Docker
docker-compose up -d

# 3. 启动开发服务器
cd backend
uv run uvicorn app.main:app --reload
```

## 推荐使用方式

### 快速开始（使用 CMD）

```cmd
# 首次设置
setup.cmd

# 启动开发服务器
start_dev.cmd
```

### 或者修改 PowerShell 策略后使用

```powershell
# 一次性设置（需要管理员权限）
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 之后就可以正常使用 PowerShell 脚本
.\setup.ps1
.\start_dev.ps1
```

## 执行策略说明

| 策略 | 说明 |
|------|------|
| Restricted | 默认策略，不允许运行任何脚本 |
| AllSigned | 只能运行由受信任的发布者签名的脚本 |
| RemoteSigned | 本地脚本可以运行，从网络下载的脚本需要签名 |
| Unrestricted | 可以运行所有脚本，但会提示确认 |
| Bypass | 不阻止任何操作，不显示警告 |

## 查看当前执行策略

```powershell
Get-ExecutionPolicy -List
```

## 安全建议

- **开发环境**: 使用 `RemoteSigned` 策略
- **生产环境**: 使用 `AllSigned` 策略
- **临时测试**: 使用 `Bypass` 仅针对当前进程

## 常见问题

### Q: 为什么会有这个限制？
A: 这是 Windows 的安全机制，防止恶意脚本自动执行。

### Q: 修改执行策略安全吗？
A: `RemoteSigned` 是安全的，它只允许本地脚本运行，网络下载的脚本需要签名。

### Q: 我没有管理员权限怎么办？
A: 使用 CMD 脚本（setup.cmd 和 start_dev.cmd）或者使用方案 4 绕过执行策略。

### Q: 每次都要输入命令太麻烦？
A: 一次性设置 `RemoteSigned` 策略后就不需要了，或者使用 CMD 脚本。

## 更多信息

- [PowerShell 执行策略官方文档](https://docs.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_execution_policies)
