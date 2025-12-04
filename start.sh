#!/bin/bash

echo "正在启动ERP系统..."
echo ""

# 检查Python是否可用
if ! command -v python &> /dev/null && ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python，请先安装Python 3.8+"
    exit 1
fi

# 确定Python命令
PYTHON_CMD="python"
if ! command -v python &> /dev/null; then
    PYTHON_CMD="python3"
fi

echo "正在检查依赖包..."
if ! $PYTHON_CMD -m pip show Flask &> /dev/null; then
    echo "正在安装依赖包..."
    $PYTHON_CMD -m pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "错误: 依赖包安装失败"
        exit 1
    fi
fi

echo ""
echo "========================================"
echo "ERP系统启动中..."
echo "访问地址: http://127.0.0.1:5000"
echo "默认管理员: admin / admin123"
echo "========================================"
echo ""

$PYTHON_CMD app.py

