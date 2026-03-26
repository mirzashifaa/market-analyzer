from typing import Any, Dict, List
from tavily import TavilyClient
from config import TAVILY_API_KEY

_client = TavilyClient(api_key=TAVILY_API_KEY)


def tavily_search(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """
    Run a Tavily search and return cleaned structured results.
    """
    response = _client.search(query=query, max_results=max_results)
    results = response.get("results", [])

    cleaned_results: List[Dict[str, Any]] = []
    for item in results:
        cleaned_results.append(
            {
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "content": item.get("content", ""),
            }
        )

    return cleaned_results


def format_search_results(results: List[Dict[str, Any]]) -> str:
    """
    Convert Tavily results into prompt-friendly text context.
    """
    formatted_chunks: List[str] = []

    for item in results:
        formatted_chunks.append(
            f"Source: {item.get('title', '')}\n"
            f"URL: {item.get('url', '')}\n"
            f"Content: {item.get('content', '')}"
        )

    return "\n\n---\n\n".join(formatted_chunks)