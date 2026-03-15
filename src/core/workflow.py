from typing import TypedDict, Annotated, Optional
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver


class ContentState(TypedDict):
    messages: list[dict]           # Full conversation history
    route: str                     # Determined route: research/blog/linkedin/image/strategy
    topic: str                     # Extracted topic from user input
    audience: str                  # Target audience
    tone: str                      # Content tone
    research_data: str             # Raw research results
    content_output: str            # Final text content output
    image_url: Optional[str]       # Generated image URL
    seo_metadata: dict             # SEO score, keywords, meta description
    quality_score: dict            # Quality validation results
    error: Optional[str]           # Error message if something failed


def build_workflow():
    from src.agents.query_handler import run_query_handler
    from src.agents.research_agent import run_research_agent
    from src.agents.blog_writer import run_blog_writer
    from src.agents.linkedin_writer import run_linkedin_writer
    from src.agents.image_generator import run_image_generator
    from src.agents.content_strategist import run_content_strategist
    from src.core.router import route_after_query_handler, route_after_research

    graph = StateGraph(ContentState)

    graph.add_node("query_handler", run_query_handler)
    graph.add_node("research_agent", run_research_agent)
    graph.add_node("blog_writer", run_blog_writer)
    graph.add_node("linkedin_writer", run_linkedin_writer)
    graph.add_node("image_generator", run_image_generator)
    graph.add_node("content_strategist", run_content_strategist)

    graph.set_entry_point("query_handler")

    graph.add_conditional_edges(
        "query_handler",
        route_after_query_handler,
        {
            "research_agent": "research_agent",
            "blog_writer": "blog_writer",
            "linkedin_writer": "linkedin_writer",
            "image_generator": "image_generator",
            "content_strategist": "content_strategist",
        },
    )

    graph.add_conditional_edges(
        "research_agent",
        route_after_research,
        {
            "blog_writer": "blog_writer",
            "content_strategist": "content_strategist",
            "__end__": END,
        },
    )

    graph.add_edge("blog_writer", END)
    graph.add_edge("linkedin_writer", END)
    graph.add_edge("image_generator", END)
    graph.add_edge("content_strategist", END)

    memory = MemorySaver()
    return graph.compile(checkpointer=memory)


app = build_workflow()
