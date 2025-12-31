#!/bin/bash

# TreeHole 生产环境启动脚本 (Ubuntu/Linux)

echo "========================================"
echo "   TreeHole 生产环境启动脚本"
echo "========================================"
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查是否为root用户
if [ "$EUID" -ne 0 ]; then
    echo -e "${YELLOW}[警告] 建议使用非root用户运行${NC}"
fi

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR/.."

# 加载环境变量
if [ -f "deploy/production.env" ]; then
    echo -e "${GREEN}[信息] 加载生产环境配置...${NC}"
    export $(cat deploy/production.env | grep -v '^#' | xargs)
else
    echo -e "${RED}[错误] 未找到 deploy/production.env 配置文件${NC}"
    echo "请先创建配置文件: cp deploy/production.env.example deploy/production.env"
    exit 1
fi

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[错误] 未检测到 Python3，请先安装: sudo apt install python3${NC}"
    exit 1
fi

# 检查 Node.js
if ! command -v node &> /dev/null; then
    echo -e "${RED}[错误] 未检测到 Node.js，请先安装${NC}"
    exit 1
fi

# 检查 npm
if ! command -v npm &> /dev/null; then
    echo -e "${RED}[错误] 未检测到 npm，请先安装${NC}"
    exit 1
fi

echo -e "${YELLOW}[信息] 正在启动后端服务...${NC}"
cd backend

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}[信息] 创建 Python 虚拟环境...${NC}"
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo -e "${RED}[错误] 虚拟环境创建失败${NC}"
        exit 1
    fi
fi

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
if [ ! -d "venv/lib/python"*"/site-packages/fastapi" ]; then
    echo -e "${YELLOW}[信息] 安装后端依赖...${NC}"
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo -e "${RED}[错误] 依赖安装失败${NC}"
        exit 1
    fi
fi

# 使用 nohup 在后台启动后端
nohup uvicorn main:app --host 0.0.0.0 --port 8000 > backend.log 2>&1 &
BACKEND_PID=$!
echo -e "${GREEN}[信息] 后端服务已启动 (PID: $BACKEND_PID)${NC}"
echo $BACKEND_PID > backend.pid

# 等待后端启动
sleep 3

# 检查后端是否启动成功
if ! curl -s http://localhost:8000/ping > /dev/null; then
    echo -e "${RED}[错误] 后端启动失败，请检查 backend/backend.log${NC}"
    exit 1
fi

echo -e "${YELLOW}[信息] 正在构建和启动前端...${NC}"
cd ../src

# 安装依赖
if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}[信息] 安装前端依赖...${NC}"
    npm install
    if [ $? -ne 0 ]; then
        echo -e "${RED}[错误] 前端依赖安装失败${NC}"
        exit 1
    fi
fi

# 构建前端生产版本
echo -e "${YELLOW}[信息] 构建前端生产版本...${NC}"
npm run build
if [ $? -ne 0 ]; then
    echo -e "${RED}[错误] 前端构建失败${NC}"
    exit 1
fi

# 使用 serve 或 nginx 提供静态文件
if command -v serve &> /dev/null; then
    # 使用 serve
    nohup serve -s dist -l 5173 > frontend.log 2>&1 &
    FRONTEND_PID=$!
    echo -e "${GREEN}[信息] 前端服务已启动 (PID: $FRONTEND_PID)${NC}"
    echo $FRONTEND_PID > frontend.pid
elif command -v python3 &> /dev/null; then
    # 使用 Python HTTP 服务器
    cd dist
    nohup python3 -m http.server 5173 > ../frontend.log 2>&1 &
    FRONTEND_PID=$!
    cd ..
    echo -e "${GREEN}[信息] 前端服务已启动 (PID: $FRONTEND_PID)${NC}"
    echo $FRONTEND_PID > frontend.pid
else
    echo -e "${YELLOW}[警告] 未找到 serve 或 python3，请手动配置前端服务${NC}"
    echo "建议安装 serve: npm install -g serve"
    echo "或使用 nginx 配置静态文件服务"
fi

# 等待前端启动
sleep 2

echo ""
echo "========================================"
echo -e "${GREEN}[成功] TreeHole 生产环境已启动！${NC}"
echo "========================================"
echo ""
echo "后端服务: http://0.0.0.0:8000"
echo "前端服务: http://0.0.0.0:5173"
echo "API文档: http://localhost:8000/docs"
echo ""
echo "后端日志: backend/backend.log"
echo "前端日志: src/frontend.log"
echo ""
echo -e "${YELLOW}[提示] 使用 ./deploy/stop-production.sh 停止服务${NC}"
echo ""
