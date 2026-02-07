@echo off
REM Skill Hub 开发服务器启动脚本 (CMD 版本)

echo === 启动 Skill Hub 开发环境 ===
echo.

REM 检查虚拟环境
if not exist ".venv" (
    echo 虚拟环境不存在，请先运行 setup.cmd
    pause
    exit /b 1
)

REM 激活虚拟环境
echo 1. 激活虚拟环境...
call .venv\Scripts\activate.bat

REM 启动 Docker 服务
echo.
echo 2. 启动 Docker 服务...
docker-compose up -d

REM 等待服务启动
echo 等待服务启动...
timeout /t 5 /nobreak >nul

REM 检查服务状态
echo.
echo 3. 检查服务状态...
docker-compose ps

REM 启动开发服务器
echo.
echo 4. 启动 FastAPI 开发服务器...
echo API 文档: http://localhost:8000/docs
echo 远程 MinIO: http://8.133.242.214:19000 (root / root10kv)
echo.
echo 按 Ctrl+C 停止服务器
echo.

cd backend
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
