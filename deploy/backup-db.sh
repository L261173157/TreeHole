#!/bin/bash

# TreeHole 数据库备份脚本
# 用法: sudo bash deploy/backup-db.sh

set -e

echo "========================================"
echo "   TreeHole 数据库备份"
echo "========================================"
echo ""

PROJECT_DIR="/opt/treehole"
cd $PROJECT_DIR

# 检查数据库是否存在
if [ ! -f "backend/treehole.db" ]; then
    echo "❌ 数据库文件不存在: backend/treehole.db"
    exit 1
fi

# 创建备份
BACKUP_FILE="backend/treehole.db.backup.$(date +%Y%m%d_%H%M%S)"
cp backend/treehole.db "$BACKUP_FILE"

# 显示备份信息
echo "✅ 数据库已备份"
echo ""
echo "📋 备份信息:"
ls -lh "$BACKUP_FILE"
echo ""

# 显示数据库统计
echo "📊 数据库统计:"
sqlite3 backend/treehole.db <<EOF
.mode column
.headers on
SELECT '留言总数:' as 信息, COUNT(*) as 数量 FROM messages;
SELECT '回复总数:' as 信息, COUNT(*) as 数量 FROM messages WHERE parent_id IS NOT NULL;
EOF

echo ""

# 清理旧备份(保留最近7天)
echo "🧹 清理旧备份(保留最近7天)..."
find backend/treehole.db.backup.* -mtime +7 -delete -print 2>/dev/null || echo "  没有需要清理的旧备份"

echo ""
echo "========================================"
echo "  备份完成!"
echo "========================================"
echo ""
echo "💾 备份文件: $BACKUP_FILE"
echo ""
echo "📂 所有备份:"
ls -lht backend/treehole.db.backup.* | head -5 || echo "  (这是第一个备份)"
echo ""
echo "💡 恢复数据库:"
echo "  sudo cp $BACKUP_FILE backend/treehole.db"
echo ""
