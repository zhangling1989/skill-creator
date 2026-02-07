# 快速启动开发服务器脚本

Write-Host "=== 启动 Skill Hub 开发环境 ===" -ForegroundColor Green

# 检查虚拟环境
if (!(Test-Path ".venv")) {
    Write-Host "虚拟环境不存在，请先运行 setup.ps1" -ForegroundColor Red
    exit 1
}

# 激活虚拟环境
Write-Host "`n1. 激活虚拟环境..." -ForegroundColor Yellow
& .venv\Scripts\Activate.ps1

# 启动 Docker 服务
Write-Host "`n2. 启动 Docker 服务..." -ForegroundColor Yellow
docker-compose up -d

# 等待服务启动
Write-Host "等待服务启动..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# 检查服务状态
Write-Host "`n3. 检查服务状态..." -ForegroundColor Yellow
docker-compose ps

# 启动开发服务器
Write-Host "`n4. 启动 FastAPI 开发服务器..." -ForegroundColor Yellow
Write-Host "API 文档: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "远程 MinIO: http://8.133.242.214:19000 (root / root10kv)" -ForegroundColor Cyan
Write-Host "`n按 Ctrl+C 停止服务器`n" -ForegroundColor Yellow

cd backend
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
