import anthropic
from src.core.config import settings

_client: anthropic.Anthropic | None = None


def get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        _client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
    return _client


def create_message(
    system: str,
    messages: list[dict],
    max_tokens: int = 4096,
    model: str | None = None,
) -> str:
    client = get_client()
    response = client.messages.create(
        model=model or settings.claude_model,
        max_tokens=max_tokens,
        system=system,
        messages=messages,
    )
    return response.content[0].text
