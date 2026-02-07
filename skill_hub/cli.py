"""命令行工具"""
import os
import sys
import subprocess
import time
import shutil
from pathlib import Path


def get_project_root():
    """获取项目根目录"""
    # 从当前文件位置向上查找项目根目录
    current = Path(__file__).resolve().parent.parent
    return current


def dev():
    """启动开发服务器"""
    print("🚀 启动 Skill Hub 开发服务器...")
    print()
    
    # 获取项目根目录
    project_root = get_project_root()
    root_env = project_root / ".env"
    backend_env = project_root / "backend" / ".env"
    docker_compose = project_root / "docker-compose.simple.yml"
    
    # 复制 .env 文件到 backend 目录
    if root_env.exists():
        print("📝 配置环境变量...")
        try:
            shutil.copy2(root_env, backend_env)
            print("✅ .env 文件已复制到 backend 目录")
        except Exception as e:
            print(f"⚠️  复制 .env 文件失败: {e}")
    else:
        print("⚠️  根目录 .env 文件不存在，请先创建")
        print(f"   位置: {root_env}")
        print("   运行: copy .env.example .env")
        return
    
    print()
    
    # 检查并启动 Docker 服务
    print("📦 检查 Docker 服务...")
    try:
        # 切换到项目根目录执行 docker-compose
        result = subprocess.run(
            ["docker-compose", "-f", str(docker_compose), "ps"],
            capture_output=True,
            text=True,
            check=False,
            cwd=str(project_root),
            encoding='utf-8',
            errors='ignore'  # 忽略编码错误
        )
        
        if "skill-hub-minio" not in result.stdout or "Up" not in result.stdout:
            print("🔄 启动 Docker 服务（MinIO + Redis）...")
            subprocess.run(
                ["docker-compose", "-f", str(docker_compose), "up", "-d"],
                check=True,
                cwd=str(project_root),
                encoding='utf-8',
                errors='ignore'
            )
            print("⏳ 等待服务启动...")
            time.sleep(5)
        else:
            print("✅ Docker 服务已运行")
    except FileNotFoundError:
        print("⚠️  Docker 未安装或 docker-compose 不可用")
        print("   请手动启动 MinIO 和 Redis")
    except Exception as e:
        print(f"⚠️  Docker 启动失败: {e}")
    
    print()
    print("📚 API 文档: http://localhost:8000/docs")
    print("🗄️  MinIO 控制台: http://localhost:9001 (minioadmin / minioadmin123)")
    print()
    print("按 Ctrl+C 停止服务器")
    print()
    
    # 切换到 backend 目录并启动服务器
    backend_dir = project_root / "backend"
    os.chdir(str(backend_dir))
    
    # 启动 uvicorn
    subprocess.run([
        sys.executable, "-m", "uvicorn",
        "app.main:app",
        "--reload",
        "--host", "0.0.0.0",
        "--port", "8000"
    ])


def start():
    """启动生产服务器"""
    print("🚀 启动 Skill Hub 生产服务器...")
    
    backend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "backend")
    os.chdir(backend_dir)
    
    subprocess.run([
        sys.executable, "-m", "uvicorn",
        "app.main:app",
        "--host", "0.0.0.0",
        "--port", "8000",
        "--workers", "4"
    ])


def db_init():
    """初始化数据库"""
    print("🗄️  初始化数据库...")
    
    sql_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "create_tables.sql")
    
    if not os.path.exists(sql_file):
        print("❌ 找不到 create_tables.sql 文件")
        return
    
    # 检查是使用本地 MySQL 还是 Docker MySQL
    print()
    print("选择数据库类型:")
    print("1. 本地 MySQL (localhost:3306)")
    print("2. Docker MySQL (localhost:3307)")
    choice = input("请选择 (1/2, 默认 1): ").strip() or "1"
    
    try:
        # 读取 SQL 文件
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        if choice == "1":
            # 使用本地 MySQL
            print()
            password = input("请输入 MySQL root 密码: ")
            
            process = subprocess.Popen(
                ["mysql", "-uroot", f"-p{password}", "skill_hub"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            stdout, stderr = process.communicate(input=sql_content)
            
            if process.returncode == 0:
                print("✅ 数据库初始化完成！")
            else:
                print(f"❌ 数据库初始化失败: {stderr}")
        else:
            # 使用 Docker MySQL
            process = subprocess.Popen(
                ["docker", "exec", "-i", "skill-hub-mysql", "mysql", "-uroot", "-proot123", "skill_hub"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            stdout, stderr = process.communicate(input=sql_content)
            
            if process.returncode == 0:
                print("✅ 数据库初始化完成！")
            else:
                print(f"❌ 数据库初始化失败: {stderr}")
    except Exception as e:
        print(f"❌ 错误: {e}")


def db_reset():
    """重置数据库"""
    print("⚠️  警告: 这将删除所有数据！")
    confirm = input("确认要重置数据库吗？(yes/no): ")
    
    if confirm.lower() != "yes":
        print("❌ 操作已取消")
        return
    
    print("🔄 重置数据库...")
    
    try:
        # 停止并删除容器
        subprocess.run(["docker-compose", "down", "-v"], check=True)
        print("✅ 容器已删除")
        
        # 重新启动
        subprocess.run(["docker-compose", "up", "-d"], check=True)
        print("✅ 容器已重启")
        
        # 等待服务启动
        print("⏳ 等待服务启动...")
        time.sleep(15)
        
        # 初始化数据库
        db_init()
        
        print("✅ 数据库重置完成！")
    except Exception as e:
        print(f"❌ 错误: {e}")


if __name__ == "__main__":
    dev()
