from src.integrations.anthropic_client import create_message
from src.integrations import openai_client

PROMPT_OPTIMIZER_SYSTEM = """You are an expert at crafting DALL-E image generation prompts.

Transform the user's topic/request into a highly detailed, optimized DALL-E 3 prompt.

Your prompt must include:
- Primary subject and composition
- Art style (e.g., professional photography, digital art, illustration, infographic style)
- Lighting and color palette
- Mood and atmosphere
- Technical details (e.g., high resolution, sharp focus, 4K)
- Negative elements to avoid (if relevant)

Keep the prompt under 400 characters. Be specific and vivid.
Output ONLY the optimized prompt, nothing else."""


def run_image_generator(state: dict) -> dict:
    topic = state.get("topic", "")
    tone = state.get("tone", "professional")

    try:
        optimized_prompt = create_message(
            system=PROMPT_OPTIMIZER_SYSTEM,
            messages=[{
                "role": "user",
                "content": f"Topic: {topic}\nTone/Style: {tone}\nCreate an optimized DALL-E prompt."
            }],
            max_tokens=200,
        )

        image_url = openai_client.generate_image(optimized_prompt.strip())

        output = (
            f"**Generated Image**\n\n"
            f"Topic: {topic}\n\n"
            f"**Optimized Prompt Used:**\n{optimized_prompt.strip()}\n\n"
            f"**Image URL:**\n{image_url}"
        )

        return {
            "content_output": output,
            "image_url": image_url,
            "error": None,
        }
    except Exception as e:
        return {
            "content_output": f"Error generating image: {str(e)}",
            "image_url": None,
            "error": str(e),
        }
