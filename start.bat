@echo off
chcp 65001 >nul
echo ========================================
echo    TreeHole 匿名留言板 - 启动脚本
echo ========================================
echo.

REM 检查 Python 是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到 Python，请先安装 Python 3.9+
    pause
    exit /b 1
)

REM 检查 Node.js 是否安装
node --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到 Node.js，请先安装 Node.js 18+
    pause
    exit /b 1
)

echo [信息] 正在启动后端服务...
cd backend

REM 检查虚拟环境是否存在
if not exist "venv\" (
    echo [信息] 创建 Python 虚拟环境...
    python -m venv venv
    if errorlevel 1 (
        echo [错误] 虚拟环境创建失败
        pause
        exit /b 1
    )
)

REM 激活虚拟环境并安装依赖
call venv\Scripts\activate
if errorlevel 1 (
    echo [错误] 虚拟环境激活失败
    pause
    exit /b 1
)

REM 检查是否需要安装依赖
if not exist "venv\Lib\site-packages\fastapi\" (
    echo [信息] 首次运行，正在安装后端依赖...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [错误] 依赖安装失败
        pause
        exit /b 1
    )
)

echo [信息] 后端服务启动中...
start "TreeHole Backend" cmd /k "cd /d %cd% && venv\Scripts\activate && uvicorn main:app --reload --host 0.0.0.0 --port 8000"

REM 等待后端启动
timeout /t 3 /nobreak >nul

echo [信息] 正在启动前端服务...
cd ..\src

REM 检查是否需要安装依赖
if not exist "node_modules\" (
    echo [信息] 首次运行，正在安装前端依赖...
    call npm install
    if errorlevel 1 (
        echo [错误] 前端依赖安装失败
        pause
        exit /b 1
    )
)

echo [信息] 前端服务启动中...
start "TreeHole Frontend" cmd /k "cd /d %cd% && npm run dev"

echo.
echo ========================================
echo [成功] TreeHole 服务已启动！
echo ========================================
echo.
echo 后端服务: http://127.0.0.1:8000
echo 前端服务: http://localhost:5173
echo API文档: http://127.0.0.1:8000/docs
echo.
echo 按任意键关闭此窗口...
pause >nul
