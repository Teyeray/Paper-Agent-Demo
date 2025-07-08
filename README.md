# Paper Agent Demo - Camel AI + FastMCP

基于 Camel AI 和 FastMCP 的论文搜索和智能代理系统。

## 项目结构

```
Paper-Agent-Demo/
├── server_camel.py      # MCP 服务器，提供论文搜索和提取功能
├── agent_camel.py       # Camel AI 智能代理
├── pyproject.toml       # 项目依赖配置
├── uv.lock             # 依赖锁定文件
├── start_server.sh      # 服务器启动脚本
├── start_agent.sh       # 代理启动脚本
├── Dockerfile.server    # 服务器 Docker 镜像
├── Dockerfile.agent     # 代理 Docker 镜像
└── docker-compose.yml   # Docker Compose 配置
```

## 功能特性

- **论文搜索**: 基于 arXiv 的智能论文搜索
- **信息提取**: 从已搜索的论文中提取详细信息
- **智能代理**: 基于 Camel AI 的对话式智能代理
- **MCP 协议**: 支持多种传输模式 (HTTP/SSE/STDIO)

## 环境要求

- Python 3.11+
- uv 包管理器
- DeepSeek API Key

## 本地安装

1. **克隆项目**
```bash
git clone <repository-url>
cd Paper-Agent-Demo
```

2. **安装依赖**
```bash
uv sync
```

3. **配置环境**
```bash
# 激活虚拟环境
source .venv/bin/activate
```

## 本地运行

### 启动服务器

```bash
# 使用启动脚本
./start_server.sh 50003 http

# 或直接运行
source .venv/bin/activate
uv run server_camel.py http
```

**参数说明:**
- `port`: 服务器端口 (默认: 50003)
- `mode`: 传输模式 (http/sse/stdio)

### 启动代理

```bash
# 使用启动脚本
./start_agent.sh YOUR_DEEPSEEK_API_KEY http://localhost:50003/my-custom-path/ http

# 或直接运行
source .venv/bin/activate
uv run agent_camel.py
```

**参数说明:**
- `api_key`: DeepSeek API 密钥
- `url`: MCP 服务器地址
- `mode`: 传输模式

## Docker 部署

### 构建镜像

```bash
# 构建服务器镜像
docker build -f Dockerfile.server -t paper-agent-server .

# 构建代理镜像
docker build -f Dockerfile.agent -t paper-agent-agent .
```

### 使用 Docker Compose

```bash
# 启动完整服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

### 单独运行容器

```bash
# 运行服务器容器
docker run -d \
  --name paper-server \
  -p 50003:50003 \
  -v $(pwd)/papers:/app/papers \
  paper-agent-server

# 运行代理容器
docker run -it \
  --name paper-agent \
  -e DEEPSEEK_API_KEY=your_api_key \
  -e MCP_URL=http://host.docker.internal:50003/my-custom-path/ \
  paper-agent-agent
```

## 使用示例

### 1. 搜索论文

```python
# 通过代理搜索论文
User: 搜索关于"machine learning"的论文，最多返回3篇
```

### 2. 提取论文信息

```python
# 提取特定论文的详细信息
User: 提取论文 "2301.12345" 的信息
```

### 3. 智能对话

```python
# 与代理进行智能对话
User: 请分析一下最近关于深度学习的趋势
```

## 配置说明

### 环境变量

- `DEEPSEEK_API_KEY`: DeepSeek API 密钥
- `MCP_URL`: MCP 服务器地址
- `PAPER_DIR`: 论文存储目录 (默认: papers)
- `PORT`: 服务器端口 (默认: 50003)

### 传输模式

- `http`: HTTP 传输模式
- `sse`: Server-Sent Events 模式
- `stdio`: 标准输入输出模式

## 开发说明

### 项目依赖

主要依赖包：
- `camel-ai>=0.2.70`: Camel AI 框架
- `fastmcp>=2.10.2`: FastMCP 协议实现
- `arxiv>=2.2.0`: arXiv API 客户端
- `fastapi>=0.116.0`: Web 框架

### 代码结构

- `server_camel.py`: MCP 服务器实现，提供论文搜索和提取工具
- `agent_camel.py`: Camel AI 智能代理，支持与 MCP 服务器交互

## 故障排除

### 常见问题

1. **依赖安装失败**
   ```bash
   uv sync --reinstall
   ```

2. **API 密钥错误**
   - 检查 DeepSeek API 密钥是否正确
   - 确认 API 密钥有足够的配额

3. **端口冲突**
   - 修改启动脚本中的端口参数
   - 检查端口是否被其他服务占用

4. **Docker 网络问题**
   - 使用 `host.docker.internal` 访问宿主机服务
   - 检查 Docker 网络配置

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！
