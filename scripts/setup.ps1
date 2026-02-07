# Skill Hub 项目快速设置脚本 (PowerShell)

Write-Host "=== Skill Hub 项目设置 ===" -ForegroundColor Green

# 检查 uv 是否安装
Write-Host "`n1. 检查 uv 是否安装..." -ForegroundColor Yellow
if (!(Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host "uv 未安装，正在安装..." -ForegroundColor Red
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    Write-Host "uv 安装完成！" -ForegroundColor Green
} else {
    Write-Host "uv 已安装" -ForegroundColor Green
}

# 创建虚拟环境
Write-Host "`n2. 创建虚拟环境..." -ForegroundColor Yellow
if (Test-Path ".venv") {
    Write-Host "虚拟环境已存在，跳过创建" -ForegroundColor Green
} else {
    uv venv
    Write-Host "虚拟环境创建完成！" -ForegroundColor Green
}

# 激活虚拟环境并安装依赖
Write-Host "`n3. 安装项目依赖..." -ForegroundColor Yellow
& .venv\Scripts\Activate.ps1
uv pip install -e .
Write-Host "依赖安装完成！" -ForegroundColor Green

# 创建 .env 文件
Write-Host "`n4. 配置环境变量..." -ForegroundColor Yellow
if (!(Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host ".env 文件已创建，请根据需要修改配置" -ForegroundColor Green
} else {
    Write-Host ".env 文件已存在" -ForegroundColor Green
}

# 检查 Docker
Write-Host "`n5. 检查 Docker..." -ForegroundColor Yellow
if (!(Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "Docker 未安装，请先安装 Docker Desktop" -ForegroundColor Red
    Write-Host "下载地址: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
} else {
    Write-Host "Docker 已安装" -ForegroundColor Green
    
    # 启动 Docker 服务
    Write-Host "`n6. 启动 Docker 服务..." -ForegroundColor Yellow
    docker-compose up -d
    Write-Host "Docker 服务启动中，请等待 10-20 秒..." -ForegroundColor Yellow
    Start-Sleep -Seconds 15
    
    # 初始化数据库
    Write-Host "`n7. 初始化数据库..." -ForegroundColor Yellow
    Get-Content create_tables.sql | docker exec -i skill-hub-mysql mysql -uroot -proot123 skill_hub
    Write-Host "数据库初始化完成！" -ForegroundColor Green
}

Write-Host "`n=== 设置完成！===" -ForegroundColor Green
Write-Host "`n下一步操作：" -ForegroundColor Yellow
Write-Host "1. 激活虚拟环境: .venv\Scripts\Activate.ps1" -ForegroundColor Cyan
Write-Host "2. 进入后端目录: cd backend" -ForegroundColor Cyan
Write-Host "3. 启动开发服务器: uv run uvicorn app.main:app --reload" -ForegroundColor Cyan
Write-Host "4. 访问 API 文档: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "5. 远程 MinIO 控制台: http://8.133.242.214:19000" -ForegroundColor Cyan
Write-Host "   用户名: root" -ForegroundColor Cyan
Write-Host "   密码: root10kv" -ForegroundColor Cyan
Write-Host "   默认存储桶: 10kv-psychology" -ForegroundColor Cyan
