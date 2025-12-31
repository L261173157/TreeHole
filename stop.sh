#!/bin/bash

# TreeHole 停止脚本 (Linux/Mac)

echo "========================================"
echo "   TreeHole 停止服务脚本"
echo "========================================"
echo ""

# 颜色定义
GREEN='\033[0;32m'
NC='\033[0m'

# 停止后端服务 (uvicorn)
echo "[信息] 正在停止后端服务..."
pkill -f "uvicorn main:app" 2>/dev/null
if [ $? -eq 0 ]; then
    echo -e "${GREEN}[成功] 后端服务已停止${NC}"
else
    echo "[提示] 后端服务未运行"
fi

# 停止前端服务 (vite)
echo "[信息] 正在停止前端服务..."
pkill -f "vite" 2>/dev/null
if [ $? -eq 0 ]; then
    echo -e "${GREEN}[成功] 前端服务已停止${NC}"
else
    echo "[提示] 前端服务未运行"
fi

echo ""
echo "========================================"
echo -e "${GREEN}[完成] TreeHole 服务已停止${NC}"
echo "========================================"
echo ""
