#!/bin/bash

# 快速部署脚本
# 用法: ./deploy.sh [local|docker] [api_key]

set -e

DEPLOY_MODE=${1:-local}
API_KEY=${2:-}

echo "=== Paper Agent Demo 部署脚本 ==="
echo "部署模式: $DEPLOY_MODE"

case $DEPLOY_MODE in
    "local")
        echo "本地部署模式"
        
        # 检查uv是否安装
        if ! command -v uv &> /dev/null; then
            echo "错误: 请先安装 uv 包管理器"
            echo "安装命令: pip install uv"
            exit 1
        fi
        
        # 安装依赖
        echo "安装依赖..."
        uv sync
        
        # 检查API密钥
        if [ -z "$API_KEY" ]; then
            echo "请输入 DeepSeek API 密钥:"
            read -s API_KEY
        fi
        
        if [ -z "$API_KEY" ] || [ "$API_KEY" = "YOUR_DEEPSEEK_API_KEY" ]; then
            echo "错误: 请提供有效的 DeepSeek API 密钥"
            exit 1
        fi
        
        echo "启动服务器..."
        ./start_server.sh 50003 http &
        SERVER_PID=$!
        
        # 等待服务器启动
        echo "等待服务器启动..."
        sleep 5
        
        echo "启动代理..."
        ./start_agent.sh "$API_KEY" "http://localhost:50003/my-custom-path/" "http"
        
        # 清理
        kill $SERVER_PID 2>/dev/null || true
        ;;
        
    "docker")
        echo "Docker 部署模式"
        
        # 检查Docker是否安装
        if ! command -v docker &> /dev/null; then
            echo "错误: 请先安装 Docker"
            exit 1
        fi
        
        # 检查docker-compose是否安装
        if ! command -v docker-compose &> /dev/null; then
            echo "错误: 请先安装 docker-compose"
            exit 1
        fi
        
        # 检查API密钥
        if [ -z "$API_KEY" ]; then
            echo "请输入 DeepSeek API 密钥:"
            read -s API_KEY
        fi
        
        if [ -z "$API_KEY" ] || [ "$API_KEY" = "YOUR_DEEPSEEK_API_KEY" ]; then
            echo "错误: 请提供有效的 DeepSeek API 密钥"
            exit 1
        fi
        
        # 设置环境变量
        export DEEPSEEK_API_KEY="$API_KEY"
        
        echo "构建并启动 Docker 服务..."
        docker-compose up --build -d
        
        echo "服务已启动!"
        echo "查看日志: docker-compose logs -f"
        echo "停止服务: docker-compose down"
        ;;
        
    *)
        echo "错误: 无效的部署模式"
        echo "用法: $0 [local|docker] [api_key]"
        echo "示例:"
        echo "  $0 local"
        echo "  $0 docker your_api_key"
        exit 1
        ;;
esac

echo "部署完成!" 