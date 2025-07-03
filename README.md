
# Paper Agent Demo / 论文智能助手演示

A simple Q&A chatbot demo based on Google SDK + FastMCP that can retrieve papers using MCP tools.

一个基于 Google SDK + FastMCP 的简单问答机器人演示，可以使用 MCP 工具来检索论文。

## 项目结构

```
paper_agent_demo/
├── agent/                  # Agent 相关代码
│   ├── paper_agent/       # 核心 agent 模块
│   ├── Dockerfile.agent   # Agent Docker 配置
│   └── start_agent.sh     # Agent 启动脚本
├── papers/                # 论文存储目录
├── server.py              # 主服务器
├── pyproject.toml         # Python 项目配置
├── uv.lock               # 依赖锁定文件
├── docker-compose.yml    # Docker Compose 配置
├── Dockerfile.server     # 服务器 Docker 配置
└── start_server.sh       # 服务器启动脚本
```

## Quick Start / 快速开始

### Docker 容器化部署 / Docker Containerized Deployment

使用 Docker 在本地启动 MCP Server 和 Agent：

1. 配置 API Key / Configure API Key：
   在 `docker-compose.yml` 文件中填入 DeepSeek API Key：

   ```yaml
   environment:
     - MCP_SERVER_URL=http://mcp-server:50003
     - DEEPSEEK_API_KEY=your_deepseek_api_key_here  # 填入您的 DeepSeek API Key
   ```
2. 启动服务 / Start Services：

   ```bash
   docker-compose up
   ```
3. 访问应用 / Access Application：
   打开浏览器访问 `http://localhost:50002`

### 分离式部署 / Separate Deployment

MCP Server 和 Agent 分开启动：

1. 配置环境 / Setup Environment：

   ```bash
   pip install -r requirements.txt
   ```
2. 配置 API Key / Configure API Key：
   在 `agent/paper_agent/agent.py` 中填入 DeepSeek API Key：

   ```python
   #Use deepseek
   os.environ['DEEPSEEK_API_KEY'] = os.getenv('DEEPSEEK_API_KEY', "your_deepseek_api_key_here")  # 填入您的 DeepSeek API Key
   ```
3. 启动 MCP Server / Start MCP Server：

   ```bash
   python server.py
   ```
4. 启动 Agent / Start Agent (在另一个终端):

   ```bash
   cd agent
   adk web
   ```
5. 访问应用 / Access Application：
   打开浏览器访问 `http://localhost:50002`

## Features / 功能特性

- **Paper Retrieval**: Search and retrieve academic papers using MCP tools / **论文检索**：使用 MCP 工具搜索和检索学术论文
- **Q&A Chat**: Interactive chatbot powered by Google SDK / **问答对话**：基于 Google SDK 的交互式聊天机器人
- **FastMCP Integration**: Seamless integration with FastMCP framework / **FastMCP 集成**：与 FastMCP 框架无缝集成
- **Docker Support**: Containerized deployment / **Docker 支持**：容器化部署
- **Modular Architecture**: Clean and extensible design / **模块化架构**：清晰可扩展的设计

## Development / 开发

This project uses uv for dependency management. Check `.python-version` for Python version requirements.

本项目使用 uv 进行依赖管理，Python 版本要求见 `.python-version` 文件。

### Tech Stack / 技术栈

- Google SDK
- FastMCP
- Python 3.x
- Docker

## Author / 作者

**Ray Yang**
Created / 创建时间：2025

## License / 许可证

MIT License

---

*A simple paper retrieval chatbot demo / 简单的论文检索聊天机器人演示*
*Created with ❤️ by Ray Yang*
