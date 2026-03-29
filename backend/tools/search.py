import asyncio
from tavily import TavilyClient

from config import TAVILY_API_KEY


client = TavilyClient(api_key=TAVILY_API_KEY)


def tavily_search(query: str, max_results: int = 5) -> list[dict]:
    """
    Synchronous Tavily search.
    """
    response = client.search(
        query=query,
        max_results=max_results,
    )
    return response.get("results", [])


async def tavily_search_async(
    query: str,
    max_results: int = 5,
) -> list[dict]:
    """
    Async wrapper around the synchronous Tavily search.
    Runs the blocking HTTP call in a worker thread.
    """
    return await asyncio.to_thread(
        tavily_search,
        query,
        max_results,
    )


def format_search_results(results: list[dict]) -> str:
    """
    Convert Tavily results into a compact plain-text format
    for agent consumption.
    """
    if not results:
        return "No relevant results found."

    formatted = []
    for i, item in enumerate(results, start=1):
        title = item.get("title", "No title")
        url = item.get("url", "No URL")
        content = item.get("content", "No content")
        formatted.append(
            f"{i}. {title}\nURL: {url}\nSummary: {content}"
        )

    return "\n\n".join(formatted)