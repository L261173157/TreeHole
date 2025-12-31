#!/bin/bash

# TreeHole 快速部署脚本 - Ubuntu服务器
# 用法: sudo ./quick-deploy.sh

set -e

echo "========================================"
echo "   TreeHole 快速部署脚本"
echo "========================================"
echo ""

# 检查是否为root
if [ "$EUID" -ne 0 ]; then
    echo "请使用 sudo 运行此脚本"
    exit 1
fi

# 获取服务器IP
SERVER_IP=$(hostname -I | awk '{print $1}')
echo "检测到服务器IP: $SERVER_IP"
echo ""

# 询问用户配置
read -p "是否使用IP地址 $SERVER_IP 访问? (y/n): " use_ip
if [ "$use_ip" != "y" ]; then
    read -p "请输入你的域名或IP: " SERVER_IP
fi

echo ""
echo "将使用以下配置:"
echo "  访问地址: http://$SERVER_IP"
echo "  前端端口: 5173"
echo "  后端端口: 8000"
echo ""
read -p "确认继续? (y/n): " confirm
if [ "$confirm" != "y" ]; then
    echo "取消部署"
    exit 0
fi

# 更新系统
echo ""
echo "[1/7] 更新系统包..."
apt update

# 安装依赖
echo "[2/7] 安装Python和Node.js..."
apt install -y python3 python3-pip python3-venv nginx curl

# 检查Node.js
if ! command -v node &> /dev/null; then
    echo "安装Node.js 18..."
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
    apt install -y nodejs
fi

# 设置项目目录
PROJECT_DIR="/opt/treehole"
echo "[3/7] 设置项目目录: $PROJECT_DIR"
mkdir -p $PROJECT_DIR

# 假设当前目录就是项目目录
echo "请确保在项目根目录运行此脚本"
CURRENT_DIR=$(pwd)

# 配置环境变量
echo "[4/7] 配置环境变量..."
cat > deploy/production.env <<EOF
CORS_ORIGINS=http://$SERVER_IP:5173,http://$SERVER_IP:8000
DATABASE_URL=sqlite:///./treehole.db
MAX_CONTENT_LENGTH=140
DEFAULT_PAGE_SIZE=20
MAX_PAGE_SIZE=100
EOF

# 安装后端依赖
echo "[5/7] 安装后端依赖..."
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate

# 安装前端依赖并构建
echo "[6/7] 构建前端..."
cd ../src
npm install
npm run build

# 配置nginx
echo "[7/7] 配置nginx..."
cat > /etc/nginx/sites-available/treehole <<EOF
server {
    listen 80;
    server_name $SERVER_IP;

    # 前端静态文件
    location / {
        root $PROJECT_DIR/src/dist;
        try_files \$uri \$uri/ /index.html;
    }

    # 后端API代理
    location /api/ {
        proxy_pass http://127.0.0.1:8000/;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    }

    # API文档(生产环境可选禁用)
    location /docs {
        proxy_pass http://127.0.0.1:8000/docs;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}
EOF

# 启用配置
ln -sf /etc/nginx/sites-available/treehole /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# 测试nginx
nginx -t

# 配置systemd服务
cat > /etc/systemd/system/treehole-backend.service <<EOF
[Unit]
Description=TreeHole Backend API
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=$PROJECT_DIR/backend
Environment="PATH=$PROJECT_DIR/backend/venv/bin"
ExecStart=$PROJECT_DIR/backend/venv/bin/uvicorn main:app --host 127.0.0.1 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# 启动服务
systemctl daemon-reload
systemctl enable treehole-backend
systemctl start treehole-backend
systemctl restart nginx

# 配置防火墙
echo ""
echo "配置防火墙..."
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 8000/tcp
ufw --force enable

echo ""
echo "========================================"
echo "  部署完成!"
echo "========================================"
echo ""
echo "访问地址:"
echo "  前端: http://$SERVER_IP"
echo "  API: http://$SERVER_IP/api/"
echo "  API文档: http://$SERVER_IP/docs"
echo ""
echo "管理命令:"
echo "  查看后端状态: sudo systemctl status treehole-backend"
echo "  重启后端: sudo systemctl restart treehole-backend"
echo "  查看日志: sudo journalctl -u treehole-backend -f"
echo "  重启nginx: sudo systemctl restart nginx"
echo ""
echo "如需HTTPS,请参考 deploy/DEPLOYMENT.md"
echo ""
