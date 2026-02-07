# Skill Hub 项目任务脚本
# 使用方法: .\tasks.ps1 <command>

param(
    [Parameter(Position=0)]
    [string]$Command = "help"
)

function Show-Help {
    Write-Host "Skill Hub 项目任务" -ForegroundColor Green
    Write-Host ""
    Write-Host "使用方法: .\tasks.ps1 <command>" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "可用命令:" -ForegroundColor Yellow
    Write-Host "  setup          - 初始化项目环境" -ForegroundColor Cyan
    Write-Host "  install        - 安装依赖" -ForegroundColor Cyan
    Write-Host "  dev            - 启动开发服务器" -ForegroundColor Cyan
    Write-Host "  docker-up      - 启动 Docker 服务" -ForegroundColor Cyan
    Write-Host "  docker-down    - 停止 Docker 服务" -ForegroundColor Cyan
    Write-Host "  docker-logs    - 查看 Docker 日志" -ForegroundColor Cyan
    Write-Host "  db-init        - 初始化数据库" -ForegroundColor Cyan
    Write-Host "  db-reset       - 重置数据库" -ForegroundColor Cyan
    Write-Host "  test           - 运行测试" -ForegroundColor Cyan
    Write-Host "  format         - 格式化代码" -ForegroundColor Cyan
    Write-Host "  lint           - 检查代码" -ForegroundColor Cyan
    Write-Host "  clean          - 清理临时文件" -ForegroundColor Cyan
    Write-Host "  help           - 显示帮助信息" -ForegroundColor Cyan
}

function Setup-Project {
    Write-Host "初始化项目..." -ForegroundColor Green
    
    # 创建虚拟环境
    if (!(Test-Path ".venv")) {
        uv venv
    }
    
    # 安装依赖
    & .venv\Scripts\Activate.ps1
    uv pip install -e ".[dev]"
    
    # 创建 .env
    if (!(Test-Path ".env")) {
        Copy-Item ".env.example" ".env"
    }
    
    Write-Host "项目初始化完成！" -ForegroundColor Green
}

function Install-Dependencies {
    Write-Host "安装依赖..." -ForegroundColor Green
    & .venv\Scripts\Activate.ps1
    uv pip install -e ".[dev]"
    Write-Host "依赖安装完成！" -ForegroundColor Green
}

function Start-Dev {
    Write-Host "启动开发服务器..." -ForegroundColor Green
    & .venv\Scripts\Activate.ps1
    docker-compose up -d
    Start-Sleep -Seconds 3
    cd backend
    uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
}

function Start-Docker {
    Write-Host "启动 Docker 服务..." -ForegroundColor Green
    docker-compose up -d
    Write-Host "Docker 服务已启动" -ForegroundColor Green
    docker-compose ps
}

function Stop-Docker {
    Write-Host "停止 Docker 服务..." -ForegroundColor Green
    docker-compose down
    Write-Host "Docker 服务已停止" -ForegroundColor Green
}

function Show-DockerLogs {
    docker-compose logs -f
}

function Init-Database {
    Write-Host "初始化数据库..." -ForegroundColor Green
    Get-Content create_tables.sql | docker exec -i skill-hub-mysql mysql -uroot -proot123 skill_hub
    Write-Host "数据库初始化完成！" -ForegroundColor Green
}

function Reset-Database {
    Write-Host "重置数据库..." -ForegroundColor Yellow
    $confirm = Read-Host "确认要重置数据库吗？所有数据将被删除！(y/N)"
    if ($confirm -eq "y" -or $confirm -eq "Y") {
        docker-compose down -v
        docker-compose up -d
        Start-Sleep -Seconds 15
        Init-Database
        Write-Host "数据库重置完成！" -ForegroundColor Green
    } else {
        Write-Host "操作已取消" -ForegroundColor Yellow
    }
}

function Run-Tests {
    Write-Host "运行测试..." -ForegroundColor Green
    & .venv\Scripts\Activate.ps1
    uv run pytest --cov=app tests/
}

function Format-Code {
    Write-Host "格式化代码..." -ForegroundColor Green
    & .venv\Scripts\Activate.ps1
    uv run black backend/app
    Write-Host "代码格式化完成！" -ForegroundColor Green
}

function Lint-Code {
    Write-Host "检查代码..." -ForegroundColor Green
    & .venv\Scripts\Activate.ps1
    uv run flake8 backend/app
}

function Clean-Project {
    Write-Host "清理临时文件..." -ForegroundColor Green
    
    # 清理 Python 缓存
    Get-ChildItem -Path . -Include __pycache__,*.pyc,*.pyo -Recurse | Remove-Item -Force -Recurse
    
    # 清理测试缓存
    if (Test-Path ".pytest_cache") { Remove-Item -Recurse -Force ".pytest_cache" }
    if (Test-Path ".coverage") { Remove-Item -Force ".coverage" }
    if (Test-Path "htmlcov") { Remove-Item -Recurse -Force "htmlcov" }
    
    Write-Host "清理完成！" -ForegroundColor Green
}

# 执行命令
switch ($Command) {
    "setup" { Setup-Project }
    "install" { Install-Dependencies }
    "dev" { Start-Dev }
    "docker-up" { Start-Docker }
    "docker-down" { Stop-Docker }
    "docker-logs" { Show-DockerLogs }
    "db-init" { Init-Database }
    "db-reset" { Reset-Database }
    "test" { Run-Tests }
    "format" { Format-Code }
    "lint" { Lint-Code }
    "clean" { Clean-Project }
    "help" { Show-Help }
    default {
        Write-Host "未知命令: $Command" -ForegroundColor Red
        Write-Host ""
        Show-Help
    }
}
