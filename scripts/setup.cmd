@echo off
REM Skill Hub 项目快速设置脚本 (CMD 版本)

echo === Skill Hub 项目设置 ===
echo.

REM 检查 uv 是否安装
echo 1. 检查 uv 是否安装...
where uv >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo uv 未安装，请先安装 uv
    echo 安装命令: pip install uv
    pause
    exit /b 1
) else (
    echo uv 已安装
)

REM 创建虚拟环境
echo.
echo 2. 创建虚拟环境...
if exist ".venv" (
    echo 虚拟环境已存在，跳过创建
) else (
    uv venv
    echo 虚拟环境创建完成！
)

REM 激活虚拟环境并安装依赖
echo.
echo 3. 安装项目依赖...
call .venv\Scripts\activate.bat
uv pip install -e .
echo 依赖安装完成！

REM 创建 .env 文件
echo.
echo 4. 配置环境变量...
if not exist ".env" (
    copy .env.example .env
    echo .env 文件已创建，请根据需要修改配置
) else (
    echo .env 文件已存在
)

REM 检查 Docker
echo.
echo 5. 检查 Docker...
where docker >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Docker 未安装，请先安装 Docker Desktop
    echo 下载地址: https://www.docker.com/products/docker-desktop
) else (
    echo Docker 已安装
    
    REM 启动 Docker 服务
    echo.
    echo 6. 启动 Docker 服务...
    docker-compose up -d
    echo Docker 服务启动中，请等待 10-20 秒...
    timeout /t 15 /nobreak >nul
    
    REM 初始化数据库
    echo.
    echo 7. 初始化数据库...
    type create_tables.sql | docker exec -i skill-hub-mysql mysql -uroot -proot123 skill_hub
    echo 数据库初始化完成！
)

echo.
echo === 设置完成！===
echo.
echo 下一步操作：
echo 1. 激活虚拟环境: .venv\Scripts\activate.bat
echo 2. 进入后端目录: cd backend
echo 3. 启动开发服务器: uv run uvicorn app.main:app --reload
echo 4. 访问 API 文档: http://localhost:8000/docs
echo 5. 远程 MinIO 控制台: http://8.133.242.214:19000
echo    用户名: root
echo    密码: root10kv
echo    默认存储桶: 10kv-psychology
echo.
pause
