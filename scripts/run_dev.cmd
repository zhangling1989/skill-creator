@echo off
REM Skill Hub 开发服务器启动脚本
REM 自动切换到项目根目录并启动服务

echo ========================================
echo   Skill Hub 开发服务器
echo ========================================
echo.

REM 获取脚本所在目录（项目根目录）
cd /d "%~dp0"

echo 当前目录: %CD%
echo.

REM 检查 .env 文件
if not exist ".env" (
    echo [错误] 找不到 .env 文件
    echo 请先创建 .env 文件: copy .env.example .env
    echo.
    pause
    exit /b 1
)

REM 复制 .env 到 backend 目录
echo [1/3] 复制配置文件...
copy /Y .env backend\.env >nul 2>&1
if errorlevel 1 (
    echo [警告] 无法复制 .env 文件到 backend 目录
) else (
    echo       ✓ 配置文件已复制
)
echo.

REM 启动 Docker 服务
echo [2/3] 启动 Docker 服务...
docker-compose -f docker-compose.simple.yml ps | findstr "Up" >nul 2>&1
if errorlevel 1 (
    echo       启动 MinIO 和 Redis...
    docker-compose -f docker-compose.simple.yml up -d
    if errorlevel 1 (
        echo [警告] Docker 启动失败，请手动启动
    ) else (
        echo       ✓ Docker 服务已启动
        timeout /t 3 /nobreak >nul
    )
) else (
    echo       ✓ Docker 服务已运行
)
echo.

REM 启动开发服务器
echo [3/3] 启动开发服务器...
echo.
echo ========================================
echo   服务地址:
echo   - API 文档: http://localhost:8000/docs
echo   - MinIO 控制台: http://localhost:9001
echo     (用户名: minioadmin / 密码: minioadmin123)
echo ========================================
echo.
echo 按 Ctrl+C 停止服务器
echo.

uv run dev
