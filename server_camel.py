import arxiv
import json
import os
from typing import List
from fastmcp import FastMCP, Context
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import PlainTextResponse
import uvicorn
import threading
import sys

# Initialize FastMCP server
mcp = FastMCP()
PAPER_DIR = os.getenv("PAPER_DIR", "papers")


@mcp.tool()
async def my_weird_add(a: int, b: int) -> int:
    r"""Adds two numbers and includes a constant offset.

    Args:
        a (int): The first number to be added.
        b (int): The second number to be added.

    Returns:
        integer: The sum of the two numbers plus 7.
    """
    return a + b + 7


@mcp.tool()
def search_papers(topic: str, max_results: int = 5) -> List[str]:
    r"""Search for papers on arXiv based on a topic and store their information.

    Args:
        topic (str): The topic to search for papers.
        max_results (int): The maximum number of results to return.

    Returns:
        List[str]: A list of paper IDs related to the topic.
    """

    # Use arxiv to find the papers
    client = arxiv.Client()
    search = arxiv.Search(
        query=topic,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance
    )
    papers = client.results(search)

    # Create directory for this topic
    path = os.path.join(PAPER_DIR, topic.lower().replace(" ", "_"))
    os.makedirs(path, exist_ok=True)
    file_path = os.path.join(path, "papers_info.json")

    # Try to load existing papers info
    try:
        with open(file_path, "r") as json_file:
            papers_info = json.load(json_file)
    except (FileNotFoundError, json.JSONDecodeError):
        papers_info = {}

    # Process each paper and add to papers_info  
    paper_ids = []
    for paper in papers:
        paper_ids.append(paper.get_short_id())
        paper_info = {
            'title': paper.title,
            'authors': [author.name for author in paper.authors],
            'summary': paper.summary,
            'pdf_url': paper.pdf_url,
            'published': str(paper.published.date())
        }
        papers_info[paper.get_short_id()] = paper_info

    # Save updated papers_info to json file
    with open(file_path, "w") as json_file:
        json.dump(papers_info, json_file, indent=2)

    print(f"Results are saved in: {file_path}")
    return paper_ids

@mcp.tool()
def extract_info(paper_id: str) -> str:
    r"""Search for information about a specific paper across all topic directories.

    Args:
        paper_id (str): The ID of the paper to extract information for.
    
    Returns:
        str: A JSON string containing the paper's information, or a message indicating no information is found.
    """
    for item in os.listdir(PAPER_DIR):
        item_path = os.path.join(PAPER_DIR, item)
        if os.path.isdir(item_path):
            file_path = os.path.join(item_path, "papers_info.json")
            if os.path.isfile(file_path):
                try:
                    with open(file_path, "r") as json_file:
                        papers_info = json.load(json_file)
                        if paper_id in papers_info:
                            return json.dumps(papers_info[paper_id], indent=2)
                except (FileNotFoundError, json.JSONDecodeError) as e:
                    print(f"Error reading {file_path}: {str(e)}")
                    continue
    return f"There's no saved information related to paper {paper_id}."



@mcp.prompt
async def generate_report_request(report_type: str, ctx: Context) -> str:
    """Generates a request for a report."""
    return f"Please create a {report_type} report. Request ID: {ctx.request_id}"



@mcp.resource("resource://config")
def get_config() -> dict:
    """Provides the application's configuration."""
    return {"version": "1.0", "author": "MyTeam"}




@mcp.resource("greetings://{name}")
def personalized_greeting(name: str) -> str:
    """Generates a personalized greeting for the given name."""
    return f"Hello, {name}! Welcome to the MCP server."



@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request) -> PlainTextResponse:
    return PlainTextResponse("OK")



def main(transport: str = "http"):
    r"""Runs the Filesystem MCP Server.
    
    Args:
        transport (str): The transport mode ('stdio' or 'sse','http').
    """
    if transport == "stdio":
        mcp.run(transport="stdio", host="0.0.0.0", port=50003, log_level="debug")
    elif transport == "sse":
        mcp.run(transport="sse", host="0.0.0.0", port=50003, path="/my-custom-sse-path", log_level= "debug")
    elif transport == "http":
        mcp.run(transport="http", host="0.0.0.0", port=50003, path="/my-custom-path", log_level="debug")
    else:
        print(f"Unknown transport mode: {transport}")


if __name__ == "__main__":
    transport_mode = sys.argv[1] if len(sys.argv) > 1 else "http"
    main(transport_mode) # runn in the defined transport mode
