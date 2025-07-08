# 快速开始指南

## 一键部署

### 本地部署
```bash
# 克隆项目
git clone <repository-url>
cd Paper-Agent-Demo

# 一键部署（需要输入API密钥）
./deploy.sh local
```

### Docker部署
```bash
# 一键部署（需要输入API密钥）
./deploy.sh docker
```

## 手动部署

### 1. 安装依赖
```bash
uv sync
```

### 2. 启动服务器
```bash
# 使用脚本启动
./start_server.sh 50003 http

# 或手动启动
source .venv/bin/activate
uv run server_camel.py http
```

### 3. 启动代理
```bash
# 使用脚本启动
./start_agent.sh YOUR_API_KEY http://localhost:50003/my-custom-path/ http

# 或手动启动
source .venv/bin/activate
uv run agent_camel.py
```

## Docker部署

### 构建镜像
```bash
# 构建服务器镜像
docker build -f Dockerfile.server -t paper-agent-server .

# 构建代理镜像
docker build -f Dockerfile.agent -t paper-agent-agent .
```

### 使用Docker Compose
```bash
# 设置环境变量
export DEEPSEEK_API_KEY=your_api_key

# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

## 使用示例

启动后，你可以与代理进行对话：

```
User: 搜索关于"machine learning"的论文，最多返回3篇
Agent: 正在搜索论文...

User: 提取论文 "2301.12345" 的信息
Agent: 正在提取论文信息...

User: 请分析一下最近关于深度学习的趋势
Agent: 基于搜索到的论文，我来分析一下...
```

## 配置说明

### 环境变量
- `DEEPSEEK_API_KEY`: DeepSeek API密钥（必需）
- `MCP_URL`: MCP服务器地址（默认: http://localhost:50003/my-custom-path/）
- `MCP_MODE`: 传输模式（默认: http）

### 传输模式
- `http`: HTTP传输模式
- `sse`: Server-Sent Events模式
- `stdio`: 标准输入输出模式

## 故障排除

1. **依赖安装失败**
   ```bash
   uv sync --reinstall
   ```

2. **API密钥错误**
   - 检查DeepSeek API密钥是否正确
   - 确认API密钥有足够的配额

3. **端口冲突**
   - 修改启动脚本中的端口参数
   - 检查端口是否被其他服务占用

4. **Docker网络问题**
   - 使用`host.docker.internal`访问宿主机服务
   - 检查Docker网络配置 