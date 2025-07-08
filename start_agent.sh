#!/bin/bash

# 代理启动脚本
# 用法: ./start_agent.sh [api_key] [url] [mode]
# 示例: ./start_agent.sh YOUR_API_KEY http://localhost:50003/my-custom-path/ http

# 检查参数数量
if [ $# -lt 3 ]; then
    echo "错误: 参数不足"
    echo "用法: $0 [api_key] [url] [mode]"
    echo "示例: $0 YOUR_API_KEY http://localhost:50003/my-custom-path/ http"
    exit 1
fi

# 获取参数
API_KEY=$1
URL=$2
MODE=$3

# 检查传输模式
if [[ ! "$MODE" =~ ^(http|sse|stdio)$ ]]; then
    echo "错误: 传输模式必须是 http, sse 或 stdio"
    echo "用法: $0 [api_key] [url] [mode]"
    exit 1
fi

# 检查API密钥
if [ -z "$API_KEY" ] || [ "$API_KEY" = "YOUR_DEEPSEEK_API_KEY" ]; then
    echo "错误: 请提供有效的 DeepSeek API 密钥"
    echo "用法: $0 [api_key] [url] [mode]"
    exit 1
fi

echo "启动 Camel AI 代理..."
echo "API 密钥: ${API_KEY:0:8}..."
echo "服务器 URL: $URL"
echo "模式: $MODE"

# 设置环境变量
export DEEPSEEK_API_KEY=$API_KEY
export MCP_URL=$URL
export MCP_MODE=$MODE

# 激活虚拟环境并启动代理
source .venv/bin/activate
uv run agent_camel.py 