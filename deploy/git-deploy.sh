#!/bin/bash

# TreeHole Git部署脚本 - 从GitHub拉取代码并部署
# 用法: sudo ./deploy/git-deploy.sh [branch]

set -e

# 配置
BRANCH=${1:-main}
PROJECT_DIR="/opt/treehole"
REPO_URL="https://github.com/YOUR_USERNAME/TreeHole.git"  # 修改为你的仓库地址

echo "========================================"
echo "   TreeHole Git部署脚本"
echo "========================================"
echo ""
echo "分支: $BRANCH"
echo "部署目录: $PROJECT_DIR"
echo ""

# 检查是否为root
if [ "$EUID" -ne 0 ]; then
    echo "请使用 sudo 运行此脚本"
    exit 1
fi

# 获取服务器IP
SERVER_IP=$(hostname -I | awk '{print $1}')
echo "服务器IP: $SERVER_IP"

# 1. 首次部署 - 安装依赖
if [ ! -d "$PROJECT_DIR" ]; then
    echo ""
    echo "[首次部署] 安装系统依赖..."
    apt update
    apt install -y python3 python3-pip python3-venv nodejs nginx git

    # 检查Node.js版本
    if ! command -v npm &> /dev/null; then
        echo "安装Node.js 18..."
        curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
        apt install -y nodejs
    fi

    echo "克隆仓库..."
    git clone -b $BRANCH $REPO_URL $PROJECT_DIR
    cd $PROJECT_DIR
else
    echo ""
    echo "[更新部署] 拉取最新代码..."
    cd $PROJECT_DIR

    # 备份数据库
    if [ -f "backend/treehole.db" ]; then
        echo "备份数据库..."
        cp backend/treehole.db backend/treehole.db.backup
    fi

    # 拉取最新代码
    git fetch origin
    git pull origin $BRANCH
fi

# 2. 配置环境变量
echo ""
echo "配置环境变量..."
if [ ! -f "deploy/production.env" ]; then
    echo "创建生产环境配置..."
    cat > deploy/production.env <<EOF
CORS_ORIGINS=http://$SERVER_IP:5173,http://$SERVER_IP:8000
DATABASE_URL=sqlite:///./treehole.db
MAX_CONTENT_LENGTH=140
DEFAULT_PAGE_SIZE=20
MAX_PAGE_SIZE=100
EOF
    echo "请编辑 deploy/production.env 配置你的域名"
fi

# 3. 安装后端依赖
echo ""
echo "安装后端依赖..."
cd backend
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install -r requirements.txt
deactivate

# 4. 构建前端
echo ""
echo "构建前端..."
cd ../src
if [ ! -d "node_modules" ]; then
    npm install
fi
npm run build

# 5. 配置nginx
echo ""
echo "配置nginx..."
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

    # API文档
    location /docs {
        proxy_pass http://127.0.0.1:8000/docs;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}
EOF

# 启用nginx配置
ln -sf /etc/nginx/sites-available/treehole /etc/nginx/sites-enabled/
nginx -t && systemctl reload nginx

# 6. 配置systemd服务
echo ""
echo "配置systemd服务..."
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

# 7. 重启服务
echo ""
echo "重启服务..."
systemctl daemon-reload
systemctl enable treehole-backend
systemctl restart treehole-backend

# 8. 配置防火墙
echo ""
echo "配置防火墙..."
ufw allow 22/tcp
ufw allow 80/tcp
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
echo "更新部署时运行:"
echo "  sudo $0 $BRANCH"
echo ""
