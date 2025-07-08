from camel.models import ModelFactory
from camel.agents import ChatAgent
from camel.types import ModelPlatformType, ModelType
from camel.configs import ChatGPTConfig
from camel.toolkits.function_tool import FunctionTool
from fastmcp.client.transports import StreamableHttpTransport, SSETransport
from fastmcp import Client
import asyncio
import os
from dotenv import load_dotenv
from camel.toolkits import MCPToolkit
import time
import requests

# 从环境变量获取配置
load_dotenv()

def ensure_mcp_url():
    url = os.getenv("MCP_URL", "")
    while True:
        if url:
            try:
                # 测试是否连通
                r = requests.get(url, timeout=3)
                if r.status_code < 500:  # MCP 服务一般返回 200/400 系列
                    break  # 合法可用，跳出循环
                else:
                    print(f"[Warning] MCP_URL responded with status code {r.status_code}")
            except Exception as e:
                print(f"[Warning] MCP_URL not reachable: {e}")
        
        # 如果 url 无效或连不上，要求手动输入
        url = input("Please input valid MCP_URL (e.g. http://localhost:50003/...): ").strip()

    os.environ["MCP_URL"] = url
    return url

mcp_url = ensure_mcp_url()
deepseek_api_key = os.getenv("DEEPSEEK_API_KEY", "YOUR_DEEPSEEK_API_KEY")
mcp_mode = os.getenv("MCP_MODE", "http")

async def main():

    config = {
        "mcpServers": {
            "my_server": {
                "url": mcp_url,  
                "mode": mcp_mode,
            }
        }
    }

    async with MCPToolkit(config_dict=config) as toolkit:
        tools_list = toolkit.get_tools()  

        sys_msg = (
            "You are a helpful assistant. Always use the provided external tools for calculation,search papers & extract information."
            "Also remember to use the tools to answer questions about the calculation. "
            "Make sure to keep the messages short and to the point so that tokens are not wasted. "
            "When asked, rather than relying on your internal knowledge. Ensure that your final answer does not "
            "end with any trailing whitespace."
        )
        model = ModelFactory.create(
            model_platform=ModelPlatformType.DEEPSEEK,
            model_type=ModelType.DEEPSEEK_CHAT,
            api_key=deepseek_api_key
        )

        agent = ChatAgent(
            system_message=sys_msg,
            model=model,
            tools=tools_list,
        )

        while True:
            user_msg = input("User: ")
            if user_msg.lower() in ["exit", "quit"]:
                break
            response = await agent.astep(user_msg)
            print(f"Agent_example: {response.msgs[0].content}\n")


if __name__ == "__main__":
    asyncio.run(main())
    print('success')