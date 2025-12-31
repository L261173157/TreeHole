#!/bin/bash

# TreeHole 手动更新脚本
# 用法: sudo bash deploy/manual-update.sh

set -e

echo "========================================"
echo "   TreeHole 手动更新脚本"
echo "========================================"
echo ""

PROJECT_DIR="/opt/treehole"
cd $PROJECT_DIR

# 检查是否为root用户
if [ "$EUID" -ne 0 ]; then
    echo "❌ 请使用 sudo 运行此脚本"
    exit 1
fi

# 0. 停止服务
echo "🛑 [0/7] 停止服务..."
systemctl stop treehole-backend

# 杀掉可能残留的uvicorn进程
if pgrep -f "uvicorn.*8000" > /dev/null; then
    echo "🔍 发现残留的uvicorn进程,正在清理..."
    pkill -9 -f "uvicorn.*8000" || true
    sleep 2
fi

echo "✅ 服务已停止"
echo ""

# 1. 备份数据库
echo "📦 [1/7] 备份数据库..."
BACKUP_FILE="backend/treehole.db.backup.$(date +%Y%m%d_%H%M%S)"
if [ -f "backend/treehole.db" ]; then
    cp backend/treehole.db "$BACKUP_FILE"
    echo "✅ 数据库已备份至: $BACKUP_FILE"
    ls -lh "$BACKUP_FILE"
else
    echo "⚠️  警告: 数据库文件不存在,跳过备份"
fi
echo ""

# 2. 拉取代码
echo "📥 [2/7] 拉取最新代码..."

# 设置超时时间为60秒
timeout 60 git fetch origin
FETCH_STATUS=$?

if [ $FETCH_STATUS -eq 124 ]; then
    echo "❌ 错误: git fetch 超时(60秒),网络连接可能存在问题"
    echo "💡 建议:"
    echo "   1. 检查网络连接"
    echo "   2. 稍后重试"
    echo "   3. 使用手动下载代码包的方式更新"
    exit 1
elif [ $FETCH_STATUS -ne 0 ]; then
    echo "❌ 错误: git fetch 失败(退出码: $FETCH_STATUS)"
    echo "💡 请检查:"
    echo "   1. 网络连接是否正常"
    echo "   2. Git仓库地址是否正确"
    echo "   3. SSH密钥或凭据配置是否正确"
    exit 1
fi

CURRENT_COMMIT=$(git rev-parse HEAD)
REMOTE_COMMIT=$(git rev-parse origin/main)

if [ "$CURRENT_COMMIT" = "$REMOTE_COMMIT" ]; then
    echo "✅ 代码已经是最新版本"
else
    echo "📝 更新内容:"
    git log HEAD..origin/main --oneline
    echo ""

    # git pull 也设置超时
    timeout 60 git pull origin main
    PULL_STATUS=$?

    if [ $PULL_STATUS -eq 124 ]; then
        echo "❌ 错误: git pull 超时(60秒)"
        exit 1
    elif [ $PULL_STATUS -ne 0 ]; then
        echo "❌ 错误: git pull 失败(退出码: $PULL_STATUS)"
        exit 1
    fi

    echo "✅ 代码已更新"
fi
echo ""

# 3. 更新后端依赖
echo "📦 [3/7] 检查后端依赖..."
cd backend
if [ ! -d "venv" ]; then
    echo "❌ 虚拟环境不存在,请先运行首次部署脚本"
    exit 1
fi

source venv/bin/activate
pip install -r requirements.txt --quiet
deactivate
cd ..
echo "✅ 后端依赖已更新"
echo ""

# 4. 构建前端
echo "🔨 [4/7] 构建前端..."
cd src
if [ ! -d "node_modules" ]; then
    echo "📦 首次构建,安装依赖..."
    npm install
fi

npm run build
if [ -d "dist" ] && [ "$(ls -A dist)" ]; then
    echo "✅ 前端构建完成"
    ls -lh dist/ | head -5
else
    echo "❌ 前端构建失败!"
    exit 1
fi
cd ..
echo ""

# 5. 启动后端
echo "🔄 [5/7] 启动后端服务..."
systemctl start treehole-backend
sleep 3

if systemctl is-active --quiet treehole-backend; then
    echo "✅ 后端服务已启动"
else
    echo "❌ 后端服务启动失败!"
    echo "📋 错误日志:"
    journalctl -u treehole-backend -n 20 --no-pager
    exit 1
fi
echo ""

# 6. 重启nginx
echo "🔄 [6/7] 重启nginx..."
systemctl restart nginx

if systemctl is-active --quiet nginx; then
    echo "✅ nginx已重启"
else
    echo "❌ nginx启动失败!"
    nginx -t
    exit 1
fi
echo ""

# 7. 验证
echo "🔍 [7/7] 验证服务状态..."
if curl -s http://localhost:8000/ping | grep -q "ok"; then
    echo "✅ 后端服务正常"
else
    echo "❌ 后端服务异常"
    echo "📋 后端日志:"
    journalctl -u treehole-backend -n 20 --no-pager
    exit 1
fi

# 清理旧备份(保留最近7天)
echo ""
echo "🧹 清理旧备份..."
find backend/treehole.db.backup.* -mtime +7 -delete 2>/dev/null || true
echo "✅ 已清理7天前的备份"

echo ""
echo "========================================"
echo "  更新完成!"
echo "========================================"
echo ""
echo "🌐 访问地址: http://123.57.82.112"
if [ -f "$BACKUP_FILE" ]; then
    echo "💾 数据库备份: $BACKUP_FILE"
fi
echo ""
echo "📊 服务状态:"
systemctl is-active treehole-backend && echo "  ✅ 后端服务: 运行中" || echo "  ❌ 后端服务: 已停止"
systemctl is-active nginx && echo "  ✅ Nginx: 运行中" || echo "  ❌ Nginx: 已停止"
echo ""
echo "📋 查看日志:"
echo "  后端: sudo journalctl -u treehole-backend -f"
echo "  Nginx: sudo tail -f /var/log/nginx/error.log"
echo ""

