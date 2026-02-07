@echo off
REM 使用本地 MySQL 启动开发服务器

echo === 启动 Skill Hub (使用本地 MySQL) ===
echo.

REM 检查虚拟环境
if not exist ".venv" (
    echo 虚拟环境不存在，请先运行: uv pip install -e .
    pause
    exit /b 1
)

REM 激活虚拟环境
echo 1. 激活虚拟环境...
call .venv\Scripts\activate.bat

REM 复制 .env 文件到 backend 目录
echo.
echo 2. 配置环境变量...
if not exist "backend\.env" (
    copy .env backend\.env
    echo .env 文件已复制到 backend 目录
) else (
    echo backend\.env 文件已存在
)

REM 只启动 Redis 和 MinIO
echo.
echo 3. 启动 Redis 和 MinIO 服务...
docker-compose -f docker-compose.simple.yml up -d

REM 等待服务启动
echo 等待服务启动...
timeout /t 3 /nobreak >nul

REM 检查服务状态
echo.
echo 4. 检查服务状态...
docker-compose -f docker-compose.simple.yml ps

REM 启动开发服务器
echo.
echo 5. 启动 FastAPI 开发服务器...
echo.
echo 注意: 使用本地 MySQL (localhost:3306) 和本地 MinIO (localhost:9000)
echo API 文档: http://localhost:8000/docs
echo MinIO 控制台: http://localhost:9001 (minioadmin / minioadmin123)
echo.
echo 按 Ctrl+C 停止服务器
echo.

cd backend
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
