#!/bin/bash

# TreeHole 生产环境停止脚本

echo "========================================"
echo "   TreeHole 停止服务"
echo "========================================"
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR/.."

# 停止后端
echo -e "${YELLOW}[信息] 正在停止后端服务...${NC}"
if [ -f "backend/backend.pid" ]; then
    BACKEND_PID=$(cat backend/backend.pid)
    if ps -p $BACKEND_PID > /dev/null 2>&1; then
        kill $BACKEND_PID
        echo -e "${GREEN}[信息] 后端服务已停止 (PID: $BACKEND_PID)${NC}"
    else
        echo -e "${YELLOW}[警告] 后端进程不存在${NC}"
    fi
    rm backend/backend.pid
else
    # 使用端口查找并停止
    BACKEND_PID=$(lsof -ti:8000 2>/dev/null)
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID
        echo -e "${GREEN}[信息] 后端服务已停止 (PID: $BACKEND_PID)${NC}"
    else
        echo -e "${YELLOW}[警告] 未找到后端服务${NC}"
    fi
fi

# 停止前端
echo -e "${YELLOW}[信息] 正在停止前端服务...${NC}"
if [ -f "src/frontend.pid" ]; then
    FRONTEND_PID=$(cat src/frontend.pid)
    if ps -p $FRONTEND_PID > /dev/null 2>&1; then
        kill $FRONTEND_PID
        echo -e "${GREEN}[信息] 前端服务已停止 (PID: $FRONTEND_PID)${NC}"
    else
        echo -e "${YELLOW}[警告] 前端进程不存在${NC}"
    fi
    rm src/frontend.pid
else
    # 使用端口查找并停止
    FRONTEND_PID=$(lsof -ti:5173 2>/dev/null)
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID
        echo -e "${GREEN}[信息] 前端服务已停止 (PID: $FRONTEND_PID)${NC}"
    else
        echo -e "${YELLOW}[警告] 未找到前端服务${NC}"
    fi
fi

echo ""
echo -e "${GREEN}[完成] 所有服务已停止${NC}"
echo ""
