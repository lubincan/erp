@echo off
echo 正在启动ERP系统...
echo.

REM 检查Python是否可用
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

echo 正在检查依赖包...
python -m pip show Flask >nul 2>&1
if errorlevel 1 (
    echo 正在安装依赖包...
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo 错误: 依赖包安装失败
        pause
        exit /b 1
    )
)

echo.
echo ========================================
echo ERP系统启动中...
echo 访问地址: http://127.0.0.1:5000
echo 默认管理员: admin / admin123
echo ========================================
echo.

python app.py

pause

