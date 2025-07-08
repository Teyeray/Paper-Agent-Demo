#!/bin/bash

# 服务器启动脚本
# 用法: ./start_server.sh [port] [mode]
# 示例: ./start_server.sh 50003 http

# 默认参数
PORT=${1:-50003}
MODE=${2:-http}

# 检查参数
if [[ ! "$MODE" =~ ^(http|sse|stdio)$ ]]; then
    echo "错误: 传输模式必须是 http, sse 或 stdio"
    echo "用法: $0 [port] [mode]"
    exit 1
fi

# 检查端口是否为数字
if ! [[ "$PORT" =~ ^[0-9]+$ ]]; then
    echo "错误: 端口必须是数字"
    echo "用法: $0 [port] [mode]"
    exit 1
fi

echo "启动 MCP 服务器..."
echo "端口: $PORT"
echo "模式: $MODE"

# 激活虚拟环境并启动服务器
source .venv/bin/activate
uv run server_camel.py $MODE 