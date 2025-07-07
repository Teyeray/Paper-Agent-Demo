import os
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv
from camel.models import ModelFactory
from camel.models.base_model import BaseModelBackend
from camel.types import ModelPlatformType, ModelType, RoleType
from camel.agents import ChatAgent
from camel.messages import BaseMessage
from camel.utils import track_agent
from camel.toolkits.function_tool import FunctionTool
import requests
import json
import logging

logger = logging.getLogger(__name__)
os.environ['DEEPSEEK_API_KEY'] = "YOUR API KEY HERE"
# Load environment variables
load_dotenv()

class MCPClient:
    """Simple MCP client to interact with MCP server."""
    
    def __init__(self, server_url: str):
        self.server_url = server_url
        self.base_url = server_url.replace('/sse', '')
    
    def search_papers(self, topic: str, max_results: int = 5) -> str:
        """Search for papers via MCP server."""
        try:
            response = requests.post(
                f"{self.base_url}/tools/search_papers",
                json={"topic": topic, "max_results": max_results},
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return json.dumps(response.json(), indent=2)
        except Exception as e:
            return f"Error searching papers: {str(e)}"
    
    def extract_info(self, paper_id: str) -> str:
        """Extract paper information via MCP server."""
        try:
            response = requests.post(
                f"{self.base_url}/tools/extract_info",
                json={"paper_id": paper_id},
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return json.dumps(response.json(), indent=2)
        except Exception as e:
            return f"Error extracting paper info: {str(e)}"

@track_agent(name="MCPPaperAgent")
class MCPPaperAgent(ChatAgent):
    """
    A paper research agent that communicates with MCP server for paper search and retrieval.
    
    This agent replaces the Google ADK implementation with Camel AI while maintaining
    the same functionality of connecting to MCP server for paper operations.
    """
    
    def __init__(
        self,
        model: Optional[BaseModelBackend] = None,
        mcp_server_url: Optional[str] = None,
        output_language: Optional[str] = "English",
    ) -> None:
        
        # Setup MCP server connection
        if mcp_server_url is None:
            mcp_server_url = os.getenv("MCP_SERVER_URL", "http://localhost:50004")
        
        self.mcp_server_url = mcp_server_url
        print(f"Connecting to MCP server: {mcp_server_url}")
        
        # Initialize MCP client
        self.mcp_client = MCPClient(mcp_server_url)
        
        # Setup model - try DeepSeek first, then fallback to Azure OpenAI
        if model is None:
            deepseek_key = os.getenv('DEEPSEEK_API_KEY')
            azure_endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
            azure_key = os.getenv('AZURE_OPENAI_API_KEY')
            
            if deepseek_key:
                model = ModelFactory.create(
                    model_platform=ModelPlatformType.DEEPSEEK,
                    model_type=ModelType.DEEPSEEK_CHAT,
                    model_config_dict={"temperature": 0.1},
                )
                print("Using DeepSeek model")
            elif azure_endpoint and azure_key:
                # For Azure OpenAI
                model = ModelFactory.create(
                    model_platform=ModelPlatformType.OPENAI,
                    model_type=ModelType.GPT_4O,
                    model_config_dict={
                        "temperature": 0.1,
                        "api_base": azure_endpoint,
                        "api_key": azure_key,
                    },
                )
                print("Using Azure OpenAI model")
            else:
                # Fallback to regular OpenAI
                model = ModelFactory.create(
                    model_platform=ModelPlatformType.OPENAI,
                    model_type=ModelType.GPT_4O_MINI,
                    model_config_dict={"temperature": 0.1},
                )
                print("Using OpenAI model")
        
        # Define system message
        system_msg = BaseMessage(
            role_name="MCP Paper Assistant",
            role_type=RoleType.ASSISTANT,
            meta_dict=None,
            content=(
                "You are an intelligent assistant capable of using external tools via MCP. "
                "You can search for papers and extract paper information using the MCP server. "
                "When users ask about papers, use the search_papers tool to find relevant papers. "
                "When users want details about a specific paper, use the extract_info tool. "
                "Always provide clear, helpful responses about the papers you find. "
                "The tools connect to an MCP server that provides access to arXiv papers."
            ),
        )
        
        # Setup tools that connect to MCP server
        tools = [
            FunctionTool(self.mcp_client.search_papers),
            FunctionTool(self.mcp_client.extract_info),
        ]
        
        super().__init__(
            system_message=system_msg,
            model=model,
            output_language=output_language,
            message_window_size=10,
            tools=tools,
        )
    
    def chat(self, message: str) -> str:
        """
        Simple chat interface for interactive use.
        
        Args:
            message: User message
            
        Returns:
            str: Agent response
        """
        user_msg = BaseMessage.make_user_message(role_name="User", content=message)
        response = self.step(user_msg)
        
        # Log tool usage
        if response.info.get('tool_calls'):
            for tool_call in response.info['tool_calls']:
                logger.info(f"Tool used: {tool_call.tool_name} with parameters: {tool_call.args}")
        
        if response.terminated:
            return "Sorry, I encountered an error processing your request."
        if not response.msgs:
            return "I didn't receive a proper response. Please try again."
            
        return response.msgs[0].content.strip()

# Create the agent instance (equivalent to the original root_agent)
def create_mcp_agent():
    """Create and return the MCP paper agent."""
    return MCPPaperAgent()

# For backward compatibility
root_agent = create_mcp_agent()

if __name__ == "__main__":
    # Interactive mode
    agent = create_mcp_agent()
    print("MCP Paper Agent is ready!")
    print("You can ask me to search for papers or get information about specific papers.")
    print("Type 'quit' to exit.\n")
    
    while True:
        try:
            user_input = input("\nUser: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            
            if not user_input:
                continue
            
            print("\nAgent: ", end="")
            response = agent.chat(user_input)
            print(response)
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")
            continue