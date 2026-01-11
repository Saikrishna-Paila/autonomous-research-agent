"""
Search Tools for Research Agent
==============================

YOUR TASK: Implement the web search tool using Tavily API

This file should contain:
1. Tavily search tool using @tool decorator
2. Optional: webpage reader tool

HINTS:
- Use langchain_core.tools.tool decorator
- Tavily client: TavilyClient(api_key=...)
- Search method: tavily.search(query=..., max_results=...)

EXAMPLE STRUCTURE:
-----------------
from langchain_core.tools import tool
from tavily import TavilyClient
from ..config import TAVILY_API_KEY, MAX_SEARCH_RESULTS

# Initialize Tavily client
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

@tool
def search_web(query: str) -> str:
    '''
    Search the web for information about any topic.

    Args:
        query: The search query

    Returns:
        Search results as formatted string
    '''
    # YOUR CODE HERE
    # 1. Call tavily_client.search(...)
    # 2. Format the results
    # 3. Return formatted string
    pass

"""

# ============================================
# YOUR CODE BELOW
# ============================================

"""
Search Tools for Research Agent

"""

from langchain_core.tools import tool
from tavily import TavilyClient
from ..config import TAVILY_API_KEY, MAX_SEARCH_RESULTS

## Initialize Tavily client

tavily_client = TavilyClient(api_key = TAVILY_API_KEY)

@tool
def search_web(query:str) -> str:
      """
      Search the web for information about any topic.
      Use this tool to find current information, news, research, and facts.
      
      Args:
          query: The search query to find information about
          
      Returns:
          Search results with titles, URLs, and content snippets
      """
      try:
            # call Tavily API
            response = tavily_client.search(
                  query= query,
                  max_results=MAX_SEARCH_RESULTS,
                  search_depth="advanced"
            )
            # format
            results = response.get("results",[]
            )
            if not results:
                  return "No results Found for this query"
            # Return detailed findings with sources for citation
            findings = []
            for i, result in enumerate(results[:4], 1):
                title = result.get('title', 'Unknown')
                url = result.get('url', '')
                content = result.get('content', '')[:500]
                findings.append(f"[Source {i}] {title}\nURL: {url}\nContent: {content}")
            return "\n\n".join(findings)
      except Exception as e:
        return f"Search error: {str(e)}"

                  





