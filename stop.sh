#!/bin/bash

# TreeHole 停止脚本 (Linux/Mac)

echo "========================================"
echo "   TreeHole 停止服务脚本"
echo "========================================"
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

BACKEND_STOPPED=0
FRONTEND_STOPPED=0

# 停止后端服务 (通过端口8000)
echo -e "${YELLOW}[信息] 正在检查后端服务 (端口8000)...${NC}"
BACKEND_PID=$(lsof -ti:8000 2>/dev/null)

if [ ! -z "$BACKEND_PID" ]; then
    echo -e "${YELLOW}[信息] 发现后端服务 PID: $BACKEND_PID${NC}"
    kill -9 $BACKEND_PID 2>/dev/null
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}[成功] 后端服务已停止 PID: $BACKEND_PID${NC}"
        BACKEND_STOPPED=1
    else
        echo -e "${RED}[警告] 停止后端服务失败 PID: $BACKEND_PID${NC}"
        # 尝试使用pkill作为备用方案
        pkill -9 -f "uvicorn main:app" 2>/dev/null
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}[成功] 使用备用方案停止后端服务${NC}"
            BACKEND_STOPPED=1
        fi
    fi
else
    echo -e "${YELLOW}[提示] 后端服务未运行或端口未被占用${NC}"
fi

echo ""

# 停止前端服务 (通过端口5173)
echo -e "${YELLOW}[信息] 正在检查前端服务 (端口5173)...${NC}"
FRONTEND_PID=$(lsof -ti:5173 2>/dev/null)

if [ ! -z "$FRONTEND_PID" ]; then
    echo -e "${YELLOW}[信息] 发现前端服务 PID: $FRONTEND_PID${NC}"
    kill -9 $FRONTEND_PID 2>/dev/null
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}[成功] 前端服务已停止 PID: $FRONTEND_PID${NC}"
        FRONTEND_STOPPED=1
    else
        echo -e "${RED}[警告] 停止前端服务失败 PID: $FRONTEND_PID${NC}"
        # 尝试使用pkill作为备用方案
        pkill -9 -f "vite" 2>/dev/null
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}[成功] 使用备用方案停止前端服务${NC}"
            FRONTEND_STOPPED=1
        fi
    fi
else
    echo -e "${YELLOW}[提示] 前端服务未运行或端口未被占用${NC}"
fi

echo ""
echo "========================================"

if [ $BACKEND_STOPPED -eq 1 ] || [ $FRONTEND_STOPPED -eq 1 ]; then
    echo -e "${GREEN}[完成] TreeHole 服务已成功停止${NC}"
else
    echo -e "${YELLOW}[提示] 没有发现运行中的TreeHole服务${NC}"
fi

echo "========================================"
echo ""
