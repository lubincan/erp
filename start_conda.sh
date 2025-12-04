#!/bin/bash

echo "========================================"
echo "ERP系统启动中 (Conda环境)"
echo "========================================"
echo ""

# 检查conda是否可用
if ! command -v conda &> /dev/null; then
    echo "[错误] 未找到conda，请先安装Anaconda或Miniconda"
    echo "或运行: bash setup_conda.sh 进行环境配置"
    exit 1
fi

# 初始化conda（如果需要）
if [ -z "$CONDA_DEFAULT_ENV" ]; then
    eval "$(conda shell.bash hook)"
fi

# 检查环境是否存在
if ! conda env list | grep -q "^erp "; then
    echo "[错误] conda环境 erp 不存在"
    echo "请先运行: bash setup_conda.sh 创建环境"
    exit 1
fi

# 激活conda环境
conda activate erp
if [ $? -ne 0 ]; then
    echo "[错误] 环境激活失败"
    exit 1
fi

# 检查依赖是否安装
if ! python -m pip show Flask &> /dev/null; then
    echo "[信息] 检测到依赖未安装，正在安装..."
    python -m pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "[错误] 依赖安装失败"
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
echo "按 Ctrl+C 停止服务器"
echo ""

# 运行应用
python app.py

