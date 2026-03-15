from src.integrations.anthropic_client import create_message

SYSTEM_PROMPT = """You are a senior content strategist at a top digital marketing agency.

Using the research provided, create a comprehensive content strategy brief.

Your strategy must include:

## 1. Executive Summary
- Topic overview (2-3 sentences)
- Key opportunity and why this content matters now

## 2. Audience Analysis
- Primary audience persona
- Pain points and motivations
- Content consumption habits

## 3. Key Themes & Messaging
- 3-5 core themes to communicate
- Primary message/angle
- Unique value proposition

## 4. Content Calendar (4-week plan)
- Week 1-4 content suggestions
- Format for each piece (blog, LinkedIn, video, infographic)
- Optimal posting cadence

## 5. SEO & Distribution Strategy
- Target keywords (5-7)
- Distribution channels
- Amplification tactics

## 6. Success Metrics
- KPIs to track
- Benchmarks to aim for

Format everything in clean, professional markdown."""


def run_content_strategist(state: dict) -> dict:
    topic = state.get("topic", "")
    audience = state.get("audience", "professionals")
    tone = state.get("tone", "professional")
    research_data = state.get("research_data", "")

    user_content = (
        f"Topic: {topic}\n"
        f"Target Audience: {audience}\n"
        f"Brand Tone: {tone}\n\n"
        f"Research Data:\n{research_data[:4000]}\n\n"
        "Create a comprehensive content strategy brief."
    )

    try:
        strategy = create_message(
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_content}],
            max_tokens=3000,
        )

        return {
            "content_output": strategy,
            "error": None,
        }
    except Exception as e:
        return {
            "content_output": f"Error generating content strategy: {str(e)}",
            "error": str(e),
        }
