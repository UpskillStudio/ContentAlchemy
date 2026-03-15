from src.integrations.anthropic_client import create_message
from src.integrations import tavily_client

SYSTEM_PROMPT = """You are an expert research analyst. Given a set of web search results,
synthesize the information into a comprehensive, well-structured research report.

Your report must include:
1. **Executive Summary** (2-3 sentences)
2. **Key Findings** (bullet points with the most important insights)
3. **Detailed Analysis** (3-5 paragraphs expanding on the findings)
4. **Data & Statistics** (any relevant numbers, percentages, or metrics found)
5. **Expert Perspectives** (quotes or viewpoints from authoritative sources if available)
6. **Sources** (list all URLs cited)

Write in clear, professional markdown. Be factual and cite specific data points."""


def _format_search_results(results: list[dict]) -> str:
    if not results:
        return "No search results found."
    lines = []
    for i, r in enumerate(results, 1):
        lines.append(f"### Result {i}: {r['title']}")
        lines.append(f"URL: {r['url']}")
        lines.append(r["content"])
        lines.append("")
    return "\n".join(lines)


def run_research_agent(state: dict) -> dict:
    topic = state.get("topic", "")
    tone = state.get("tone", "professional")

    try:
        search_results = tavily_client.search(topic)
        formatted_results = _format_search_results(search_results)

        user_content = (
            f"Topic: {topic}\n"
            f"Tone: {tone}\n\n"
            f"Search Results:\n{formatted_results}\n\n"
            "Please synthesize these results into a comprehensive research report."
        )

        report = create_message(
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_content}],
            max_tokens=2048,
        )

        return {
            "research_data": report,
            "content_output": report,
            "error": None,
        }
    except Exception as e:
        fallback = f"Research on '{topic}': Unable to fetch live data. Error: {str(e)}"
        return {
            "research_data": fallback,
            "content_output": fallback,
            "error": str(e),
        }
