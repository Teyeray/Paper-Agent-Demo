#!/bin/bash

echo "🚀 Starting MCP Server..."

# 激活 uv 创建的虚拟环境
source .venv/bin/activate

# 检查依赖是否安装
echo "📦 Checking dependencies..."
python -c "import arxiv, mcp; print('✅ Dependencies OK')" || {
    echo "❌ Dependencies missing!"
    exit 1
}

# 启动服务器
echo "Starting server on 0.0.0.0:8001..."
python server.py