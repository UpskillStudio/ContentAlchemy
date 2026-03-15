from openai import OpenAI
from src.core.config import settings

_client: OpenAI | None = None


def get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(api_key=settings.openai_api_key)
    return _client


def generate_image(prompt: str, size: str | None = None, quality: str | None = None) -> str:
    client = get_client()
    response = client.images.generate(
        model=settings.dalle_model,
        prompt=prompt,
        size=size or settings.image_size,
        quality=quality or settings.image_quality,
        n=1,
    )
    return response.data[0].url
