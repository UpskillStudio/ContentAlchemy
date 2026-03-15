import yaml
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import Field

load_dotenv()


class Settings(BaseSettings):
    anthropic_api_key: str = Field(...)
    tavily_api_key: str = Field(...)
    openai_api_key: str = Field(...)

    claude_model: str = "claude-sonnet-4-6"
    dalle_model: str = "dall-e-3"
    image_size: str = "1024x1024"
    image_quality: str = "standard"

    research_max_results: int = 5
    blog_min_words: int = 800
    blog_max_words: int = 1500
    linkedin_max_chars: int = 3000
    linkedin_hashtag_count: int = 5
    max_retries: int = 3

    model_config = {"env_file": ".env", "extra": "ignore"}


def load_yaml_config() -> dict:
    config_path = Path(__file__).parent.parent.parent / "config" / "settings.yaml"
    if config_path.exists():
        with open(config_path) as f:
            return yaml.safe_load(f)
    return {}


settings = Settings()
yaml_config = load_yaml_config()
