#!/bin/bash

# TreeHole 启动脚本 (Linux/Mac)

echo "========================================"
echo "   TreeHole 匿名留言板 - 启动脚本"
echo "========================================"
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查 Python 是否安装
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[错误] 未检测到 Python3，请先安装 Python 3.9+${NC}"
    exit 1
fi

# 检查 Node.js 是否安装
if ! command -v node &> /dev/null; then
    echo -e "${RED}[错误] 未检测到 Node.js，请先安装 Node.js 18+${NC}"
    exit 1
fi

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# 启动后端
echo -e "${YELLOW}[信息] 正在启动后端服务...${NC}"
cd backend

# 检查虚拟环境是否存在
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

# 检查是否需要安装依赖
if [ ! -d "venv/lib/python"*"/site-packages/fastapi" ]; then
    echo -e "${YELLOW}[信息] 首次运行，正在安装后端依赖...${NC}"
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo -e "${RED}[错误] 依赖安装失败${NC}"
        exit 1
    fi
fi

# 在新终端窗口启动后端
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    osascript -e "tell application \"Terminal\" to do script \"cd $(pwd) && source venv/bin/activate && uvicorn main:app --reload --host 0.0.0.0 --port 8000\"" > /dev/null 2>&1 &
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    if command -v gnome-terminal &> /dev/null; then
        gnome-terminal -- bash -c "cd $(pwd) && source venv/bin/activate && uvicorn main:app --reload --host 0.0.0.0 --port 8000; exec bash" &
    elif command -v xterm &> /dev/null; then
        xterm -e "cd $(pwd) && source venv/bin/activate && uvicorn main:app --reload --host 0.0.0.0 --port 8000" &
    else
        # 后台运行
        nohup uvicorn main:app --reload --host 0.0.0.0 --port 8000 > backend.log 2>&1 &
        echo -e "${GREEN}[信息] 后端已在后台运行，日志文件: backend/backend.log${NC}"
    fi
fi

# 等待后端启动
sleep 3

# 启动前端
echo -e "${YELLOW}[信息] 正在启动前端服务...${NC}"
cd ../src

# 检查是否需要安装依赖
if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}[信息] 首次运行，正在安装前端依赖...${NC}"
    npm install
    if [ $? -ne 0 ]; then
        echo -e "${RED}[错误] 前端依赖安装失败${NC}"
        exit 1
    fi
fi

# 在新终端窗口启动前端
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    osascript -e "tell application \"Terminal\" to do script \"cd $(pwd) && npm run dev\"" > /dev/null 2>&1 &
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    if command -v gnome-terminal &> /dev/null; then
        gnome-terminal -- bash -c "cd $(pwd) && npm run dev; exec bash" &
    elif command -v xterm &> /dev/null; then
        xterm -e "cd $(pwd) && npm run dev" &
    else
        # 后台运行
        nohup npm run dev > frontend.log 2>&1 &
        echo -e "${GREEN}[信息] 前端已在后台运行，日志文件: src/frontend.log${NC}"
    fi
fi

echo ""
echo "========================================"
echo -e "${GREEN}[成功] TreeHole 服务已启动！${NC}"
echo "========================================"
echo ""
echo "后端服务: http://127.0.0.1:8000"
echo "前端服务: http://localhost:5173"
echo "API文档: http://127.0.0.1:8000/docs"
echo ""
