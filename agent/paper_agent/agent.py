import os
import asyncio
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import SseServerParams
from google.adk.runners import InMemoryRunner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import FunctionTool
from typing import Any, Dict
import openai

# Set environment variables if needed

#Use deepseek
os.environ['DEEPSEEK_API_KEY'] = os.getenv('DEEPSEEK_API_KEY', "")

#Use gpt-4o
os.environ["AZURE_OPENAI_ENDPOINT"] = os.getenv("AZURE_OPENAI_ENDPOINT", "")
os.environ["AZURE_OPENAI_API_KEY"] = os.getenv("AZURE_OPENAI_API_KEY", "")
os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"] = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "")

# 根据环境选择 MCP 服务器地址
mcp_server_url = os.getenv("MCP_SERVER_URL", "http://localhost:8001")
print(f"Connecting to MCP server: {mcp_server_url}")

# Configure connection
toolset = MCPToolset(
    connection_params=SseServerParams(
        url=f"{mcp_server_url}/sse",
    ),
)

model = LiteLlm(model="deepseek/deepseek-chat")

# Create agent
root_agent = Agent(
    name="mcp_sse_agent",
    model=model,
    instruction="You are an intelligent assistant capable of using external tools via MCP. You can search for papers and extract paper information.",
    tools=[toolset]
)