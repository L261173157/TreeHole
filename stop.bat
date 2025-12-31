@echo off
chcp 65001 >nul
echo ========================================
echo    TreeHole 停止服务脚本
echo ========================================
echo.

set "BACKEND_STOPPED=0"
set "FRONTEND_STOPPED=0"

REM 停止后端服务 (端口8000)
echo [信息] 正在检查后端服务 (端口8000)...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do (
    echo [信息] 发现后端服务 PID: %%a
    taskkill /PID %%a /F >nul 2>&1
    if errorlevel 1 (
        echo [警告] 停止后端服务失败 PID: %%a
    ) else (
        echo [成功] 后端服务已停止 PID: %%a
        set "BACKEND_STOPPED=1"
    )
)

if %BACKEND_STOPPED%==0 (
    echo [提示] 后端服务未运行或端口未被占用
)

echo.

REM 停止前端服务 (端口5173)
echo [信息] 正在检查前端服务 (端口5173)...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5173 ^| findstr LISTENING') do (
    echo [信息] 发现前端服务 PID: %%a
    taskkill /PID %%a /F >nul 2>&1
    if errorlevel 1 (
        echo [警告] 停止前端服务失败 PID: %%a
    ) else (
        echo [成功] 前端服务已停止 PID: %%a
        set "FRONTEND_STOPPED=1"
    )
)

if %FRONTEND_STOPPED%==0 (
    echo [提示] 前端服务未运行或端口未被占用
)

echo.
echo ========================================
echo [完成] TreeHole 服务停止操作完成
echo ========================================
echo.
pause
