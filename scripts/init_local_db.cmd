@echo off
REM 在本地 MySQL 中初始化数据库

echo === 初始化本地 MySQL 数据库 ===
echo.

echo 请输入你的 MySQL root 密码:
set /p MYSQL_PASSWORD=

echo.
echo 1. 创建数据库...
mysql -u root -p%MYSQL_PASSWORD% -e "CREATE DATABASE IF NOT EXISTS skill_hub CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

echo.
echo 2. 执行建表脚本...
mysql -u root -p%MYSQL_PASSWORD% skill_hub < create_tables.sql

echo.
echo ✅ 数据库初始化完成！
echo.
echo 数据库信息:
echo - 数据库名: skill_hub
echo - 主机: localhost:3306
echo - 用户: root
echo.
pause
