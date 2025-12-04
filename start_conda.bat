@echo off
echo ========================================
echo ERP系统启动中 (Conda环境)
echo ========================================
echo.

REM 检查conda是否可用
conda --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到conda，请先安装Anaconda或Miniconda
    echo 或运行: setup_conda.bat 进行环境配置
    pause
    exit /b 1
)

REM 检查环境是否存在
conda env list | findstr /C:"erp" >nul 2>&1
if errorlevel 1 (
    echo [错误] conda环境 erp 不存在
    echo 请先运行: setup_conda.bat 创建环境
    pause
    exit /b 1
)

REM 设置conda环境Python路径
set CONDA_PYTHON=C:\Users\Lucas\.conda\envs\erp\python.exe

REM 检查conda环境是否存在
if not exist "%CONDA_PYTHON%" (
    echo [错误] conda环境 erp 不存在
    echo 请先运行: setup_conda.bat 创建环境
    pause
    exit /b 1
)

REM 检查依赖是否安装
"%CONDA_PYTHON%" -m pip show Flask >nul 2>&1
if errorlevel 1 (
    echo [信息] 检测到依赖未安装，正在安装...
    "%CONDA_PYTHON%" -m pip install -r requirements.txt
    if errorlevel 1 (
        echo [错误] 依赖安装失败
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
echo 按 Ctrl+C 停止服务器
echo.

REM 运行应用
"%CONDA_PYTHON%" app.py

REM 如果应用退出，保持窗口打开
pause

