#!/bin/bash

echo "========================================"
echo "ERP系统 - Conda环境配置脚本"
echo "========================================"
echo ""

# 检查conda是否可用
if ! command -v conda &> /dev/null; then
    echo "[错误] 未找到conda，请先安装Anaconda或Miniconda"
    echo "下载地址: https://www.anaconda.com/products/distribution"
    exit 1
fi

# 初始化conda（如果需要）
if [ -z "$CONDA_DEFAULT_ENV" ]; then
    eval "$(conda shell.bash hook)"
fi

echo "[1/3] 检查conda环境..."
if conda env list | grep -q "^erp "; then
    echo "[信息] 环境 erp 已存在，更新环境..."
    conda env update -f environment.yml --prune
    if [ $? -ne 0 ]; then
        echo "[警告] 环境更新可能有问题，但可以继续"
    fi
else
    echo "[2/3] 创建conda虚拟环境: erp"
    conda env create -f environment.yml
    if [ $? -ne 0 ]; then
        echo "[错误] 环境创建失败"
        exit 1
    fi
    echo "[成功] 环境创建完成"
fi

echo "[3/3] 环境配置完成！"
echo ""
echo "========================================"
echo "[成功] Conda环境配置完成！"
echo "========================================"
echo ""
echo "使用以下命令激活环境并运行项目："
echo "  conda activate erp"
echo "  python app.py"
echo ""
echo "或直接运行: bash start_conda.sh"
echo ""

