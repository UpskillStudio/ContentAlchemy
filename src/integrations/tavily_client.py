from tavily import TavilyClient
from src.core.config import settings

_client: TavilyClient | None = None


def get_client() -> TavilyClient:
    global _client
    if _client is None:
        _client = TavilyClient(api_key=settings.tavily_api_key)
    return _client


def search(query: str, max_results: int | None = None) -> list[dict]:
    client = get_client()
    n = max_results or settings.research_max_results
    response = client.search(
        query=query,
        search_depth="advanced",
        max_results=n,
        include_answer=True,
    )
    results = []
    for r in response.get("results", []):
        results.append({
            "title": r.get("title", ""),
            "url": r.get("url", ""),
            "content": r.get("content", ""),
        })
    return results


def get_answer(query: str) -> str:
    client = get_client()
    response = client.search(query=query, search_depth="advanced", max_results=3, include_answer=True)
    return response.get("answer", "")
