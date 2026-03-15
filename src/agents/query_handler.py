import json
import re
from src.integrations.anthropic_client import create_message

SYSTEM_PROMPT = """You are an intelligent content request router for a content marketing platform.

Analyze the user's request and extract:
1. The best content route
2. The main topic
3. Target audience
4. Desired tone

ROUTES (choose exactly one):
- "research"  → User wants deep research, facts, analysis, or a report on a topic
- "blog"      → User wants a blog post, article, or long-form written content
- "linkedin"  → User wants a LinkedIn post, social media content, or professional update
- "image"     → User wants an image, visual, infographic, or illustration
- "strategy"  → User wants a content strategy, content calendar, or content plan

Respond ONLY with valid JSON in this exact format:
{
  "route": "<research|blog|linkedin|image|strategy>",
  "topic": "<concise topic description>",
  "audience": "<target audience, default: general professionals>",
  "tone": "<professional|conversational|technical|inspirational|educational>"
}"""


def run_query_handler(state: dict) -> dict:
    messages = state.get("messages", [])
    if not messages:
        return {"error": "No messages provided", "route": "research"}

    last_user_message = next(
        (m["content"] for m in reversed(messages) if m["role"] == "user"), ""
    )

    try:
        response = create_message(
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": last_user_message}],
            max_tokens=256,
        )
        cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", response.strip(), flags=re.MULTILINE)
        parsed = json.loads(cleaned)
        route = parsed.get("route", "research")
        if route not in {"research", "blog", "linkedin", "image", "strategy"}:
            route = "research"

        return {
            "route": route,
            "topic": parsed.get("topic", last_user_message),
            "audience": parsed.get("audience", "general professionals"),
            "tone": parsed.get("tone", "professional"),
            "error": None,
        }
    except (json.JSONDecodeError, Exception) as e:
        return {
            "route": "research",
            "topic": last_user_message,
            "audience": "general professionals",
            "tone": "professional",
            "error": f"Query handler error: {str(e)}",
        }
