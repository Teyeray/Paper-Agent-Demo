#!/bin/bash

echo "🚀 Starting ADK Web Interface..."
export MCP_SERVER_URL=${MCP_SERVER_URL:-"http://localhost:50003"}
# 激活 uv 创建的虚拟环境
source .venv/bin/activate

# 等待 MCP Server 启动
# echo "⏳ Waiting for MCP Server..."
# sleep 5

# 检查 MCP Server 是否可用
# echo "🔍 Checking MCP Server connection..."
# max_retries=30
# retry_count=0

# while [ $retry_count -lt $max_retries ]; do
#     if curl -s http://mcp-server:8001/sse > /dev/null 2>&1; then
#         echo "✅ MCP Server is available"
#         break
#     fi
#     echo "⏳ Waiting for MCP Server... ($((retry_count + 1))/$max_retries)"
#     sleep 2
#     retry_count=$((retry_count + 1))
# done

# if [ $retry_count -eq $max_retries ]; then
#     echo "❌ MCP Server is not available after waiting"
#     exit 1
# fi
# 检查目录结构
echo "📁 Checking directory structure..."
ls -la
ls -la paper_agent/

# 启动 ADK Web Interface
echo "----------Starting ADK Web on 0.0.0.0:50002...------------"
adk web --host 0.0.0.0 --port 50002