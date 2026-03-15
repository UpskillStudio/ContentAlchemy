from src.integrations.anthropic_client import create_message
from src.utils.quality_validation import validate_content
from src.core.config import settings

SYSTEM_PROMPT = """You are a LinkedIn content expert and personal branding specialist.

Create an engaging LinkedIn post following these requirements:

STRUCTURE:
1. Hook (first 1-2 lines must be compelling — readers see this before "see more")
2. Body (the main insight, story, or value — short paragraphs, 1-3 sentences each)
3. Call to action (ask a question or invite engagement)
4. Hashtags (5 relevant hashtags on a separate line at the end)

FORMATTING:
- Use line breaks generously (LinkedIn doesn't render markdown)
- Use emojis sparingly for visual breaks (1-3 max)
- Keep paragraphs to 1-3 sentences
- Total length: 150-300 words (sweet spot for engagement)
- NO markdown headers or bullet point symbols — use plain text with line breaks

CONTENT PRINCIPLES:
- Lead with a bold statement, surprising fact, or personal story hook
- Provide genuine value or insight
- Be conversational, not corporate
- Include one concrete takeaway or lesson
- End with an engaging question to drive comments

HASHTAG STRATEGY:
- Mix 2 broad hashtags (#AI, #Leadership) + 3 niche hashtags
- Place hashtags at the very end"""


def run_linkedin_writer(state: dict) -> dict:
    topic = state.get("topic", "")
    audience = state.get("audience", "professionals")
    tone = state.get("tone", "professional")
    research_data = state.get("research_data", "")

    context = f"\nContext from research:\n{research_data[:1500]}" if research_data else ""

    user_content = (
        f"Topic: {topic}\n"
        f"Target Audience: {audience}\n"
        f"Tone: {tone}\n"
        f"Hashtag count: {settings.linkedin_hashtag_count}"
        f"{context}\n\n"
        "Please write an engaging LinkedIn post."
    )

    try:
        post = create_message(
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_content}],
            max_tokens=800,
        )
        quality = validate_content(post, "linkedin")

        return {
            "content_output": post,
            "quality_score": quality,
            "error": None,
        }
    except Exception as e:
        return {
            "content_output": f"Error generating LinkedIn post: {str(e)}",
            "quality_score": {},
            "error": str(e),
        }
