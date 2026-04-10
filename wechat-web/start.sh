#!/bin/bash

# 微信公众号文章排版发布工具 - 启动脚本

echo "=========================================="
echo "🚀 微信公众号文章排版发布工具"
echo "=========================================="

# 检查 Python 版本
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "📌 Python 版本: $PYTHON_VERSION"

# 检查依赖
echo ""
echo "📦 检查依赖..."
if pip show flask > /dev/null 2>&1; then
    echo "✅ Flask 已安装"
else
    echo "📥 正在安装 Flask..."
    pip install -r requirements.txt
fi

if pip show python-docx > /dev/null 2>&1; then
    echo "✅ python-docx 已安装"
else
    pip install python-docx
fi

if pip show Pillow > /dev/null 2>&1; then
    echo "✅ Pillow 已安装"
else
    pip install Pillow
fi

echo ""
echo "=========================================="
echo "🌐 启动服务中..."
echo "=========================================="
echo ""
echo "📍 访问地址: http://127.0.0.1:5000"
echo "📍 或访问: http://localhost:5000"
echo ""
echo "按 Ctrl+C 停止服务"
echo "=========================================="

# 启动 Flask
python3 app.py
