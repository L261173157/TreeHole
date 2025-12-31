@echo off
chcp 65001 >nul
echo ========================================
echo    TreeHole 停止服务脚本
echo ========================================
echo.

echo [信息] 正在停止后端服务...
for /f "tokens=2" %%i in ('tasklist /fi "imagename eq python.exe" ^| find "python.exe"') do taskkill /PID %%i /F >nul 2>&1

echo [信息] 正在停止前端服务...
for /f "tokens=2" %%i in ('tasklist /fi "imagename eq node.exe" ^| find "node.exe"') do taskkill /PID %%i /F >nul 2>&1

echo.
echo ========================================
echo [成功] TreeHole 服务已停止
echo ========================================
echo.
pause
