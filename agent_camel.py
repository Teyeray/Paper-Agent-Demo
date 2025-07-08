from camel.models import ModelFactory
from camel.agents import ChatAgent
from camel.types import ModelPlatformType, ModelType
from camel.configs import ChatGPTConfig
from camel.toolkits.function_tool import FunctionTool
from fastmcp.client.transports import StreamableHttpTransport, SSETransport
from fastmcp import Client
import asyncio
import os

from camel.toolkits import MCPToolkit

# 从环境变量获取配置
deepseek_api_key = os.getenv("DEEPSEEK_API_KEY", "YOUR_DEEPSEEK_API_KEY")
mcp_url = os.getenv("MCP_URL", "http://localhost:50003/my-custom-path/")
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