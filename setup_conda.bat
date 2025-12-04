@echo off
echo ========================================
echo ERP系统 - Conda环境配置脚本
echo ========================================
echo.

REM 检查conda是否可用
conda --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到conda，请先安装Anaconda或Miniconda
    echo 下载地址: https://www.anaconda.com/products/distribution
    pause
    exit /b 1
)

echo [1/3] 检查conda环境...
conda env list | findstr /C:"erp" >nul 2>&1
if errorlevel 1 (
    echo [2/3] 创建conda虚拟环境: erp
    conda env create -f environment.yml
    if errorlevel 1 (
        echo [错误] 环境创建失败
        pause
        exit /b 1
    )
    echo [成功] 环境创建完成
) else (
    echo [信息] 环境 erp 已存在，跳过创建
    echo [2/3] 更新conda环境...
    conda env update -f environment.yml --prune
    if errorlevel 1 (
        echo [警告] 环境更新可能有问题，但可以继续
    )
)

echo [3/3] 激活环境并安装依赖...
call conda activate erp
if errorlevel 1 (
    echo [错误] 环境激活失败
    pause
    exit /b 1
)

echo.
echo ========================================
echo [成功] Conda环境配置完成！
echo ========================================
echo.
echo 使用以下命令激活环境并运行项目：
echo   conda activate erp
echo   python app.py
echo.
echo 或直接运行: start_conda.bat
echo.
pause

