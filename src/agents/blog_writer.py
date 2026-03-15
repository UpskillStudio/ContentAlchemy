from src.integrations.anthropic_client import create_message
from src.utils.content_optimization import calculate_seo_score, extract_keywords, generate_meta_description
from src.utils.quality_validation import validate_content
from src.core.config import settings

SYSTEM_PROMPT = """You are an expert SEO content writer and digital marketing specialist.

Create a comprehensive, SEO-optimized blog post following these requirements:

STRUCTURE:
- Compelling title with primary keyword (H1)
- Engaging introduction with hook (150-200 words)
- 3-5 main sections with H2 headers
- Subsections with H3 headers where appropriate
- Conclusion with clear CTA
- Total length: 800-1500 words

SEO REQUIREMENTS:
- Use primary keyword in title, first paragraph, and 2-3 H2 headers
- Include LSI (Latent Semantic Indexing) keywords naturally
- Write meta description (150-160 characters) at the top
- Include estimated read time
- Use bullet points and numbered lists for scannability

WRITING STYLE:
- Match the specified tone and audience
- Use active voice
- Short paragraphs (3-4 sentences max)
- Include transition words for flow
- Add data, statistics, and examples for credibility

Format the output in clean Markdown."""


def run_blog_writer(state: dict) -> dict:
    topic = state.get("topic", "")
    audience = state.get("audience", "general professionals")
    tone = state.get("tone", "professional")
    research_data = state.get("research_data", "")

    research_section = ""
    if research_data:
        research_section = f"\n\nRESEARCH DATA TO INCORPORATE:\n{research_data[:3000]}"

    user_content = (
        f"Topic: {topic}\n"
        f"Target Audience: {audience}\n"
        f"Tone: {tone}\n"
        f"Word Count Target: {settings.blog_min_words}-{settings.blog_max_words} words"
        f"{research_section}\n\n"
        "Please write a complete, SEO-optimized blog post."
    )

    try:
        blog_content = create_message(
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_content}],
            max_tokens=3000,
        )

        seo_metadata = {
            "seo_score": calculate_seo_score(blog_content),
            "keywords": extract_keywords(blog_content),
            "meta_description": generate_meta_description(blog_content),
        }
        quality = validate_content(blog_content, "blog")

        return {
            "content_output": blog_content,
            "seo_metadata": seo_metadata,
            "quality_score": quality,
            "error": None,
        }
    except Exception as e:
        return {
            "content_output": f"Error generating blog post: {str(e)}",
            "seo_metadata": {},
            "quality_score": {},
            "error": str(e),
        }
