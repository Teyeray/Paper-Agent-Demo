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

### Using Docker Compose / 使用 Docker Compose

```bash
docker-compose up
```

### Manual Setup / 手动设置

1. Install dependencies / 安装依赖：
```bash
uv pip install -r pyproject.toml
```

2. Start server / 启动服务器：
```bash
./start_server.sh
```

3. Start agent / 启动智能助手：
```bash
cd agent && ./start_agent.sh
```

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


