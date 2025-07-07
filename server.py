import arxiv
import json
import os
from typing import List
from mcp.server.fastmcp import FastMCP
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import threading

PAPER_DIR = "papers"

# Initialize FastMCP server
mcp = FastMCP("research", host="0.0.0.0", port=50003)

# Add HTTP API support
app = FastAPI(title="Paper Research MCP Server")

# Request models
class SearchRequest(BaseModel):
    topic: str
    max_results: int = 5

class ExtractRequest(BaseModel):
    paper_id: str

@mcp.tool()
def search_papers(topic: str, max_results: int = 5) -> List[str]:
    """Search for papers on arXiv based on a topic and store their information."""
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
    """Search for information about a specific paper across all topic directories."""
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

# HTTP endpoints
@app.post("/tools/search_papers")
async def api_search_papers(request: SearchRequest):
    """HTTP endpoint for searching papers."""
    try:
        result = search_papers(request.topic, request.max_results)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tools/extract_info")
async def api_extract_info(request: ExtractRequest):
    """HTTP endpoint for extracting paper info."""
    try:
        result = extract_info(request.paper_id)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

def run_http_server():
    """Run the HTTP server."""
    uvicorn.run(app, host="0.0.0.0", port=50004)

if __name__ == "__main__":
    # Start HTTP server in a separate thread
    http_thread = threading.Thread(target=run_http_server, daemon=True)
    http_thread.start()
    
    print("HTTP API server started on port 50004")   #use for camel
    print("MCP SSE server starting on port 50003")
    
    # Run MCP server
    mcp.run(transport="sse")