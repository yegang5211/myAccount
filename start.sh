#!/bin/bash

echo "启动我的记账本..."
echo

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误：未找到Python3，请先安装Python 3.8+"
    exit 1
fi

# 检查是否在虚拟环境中
if [ -z "$VIRTUAL_ENV" ]; then
    echo "建议使用虚拟环境，正在检查是否存在venv..."
    if [ -f "venv/bin/activate" ]; then
        echo "发现虚拟环境，正在激活..."
        source venv/bin/activate
    else
        echo "未找到虚拟环境，使用系统Python环境"
    fi
fi

# 检查依赖是否安装
echo "检查依赖包..."
if ! pip show streamlit &> /dev/null; then
    echo "正在安装依赖包..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "错误：依赖包安装失败"
        exit 1
    fi
fi

# 启动应用
echo "启动Streamlit应用..."
echo "应用将在浏览器中自动打开"
echo "如果没有自动打开，请访问：http://localhost:8501"
echo
echo "按 Ctrl+C 停止应用"
echo

streamlit run app.py
