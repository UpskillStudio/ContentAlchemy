from typing import Literal


VALID_ROUTES = {"research", "blog", "linkedin", "image", "strategy"}


def route_after_query_handler(state: dict) -> Literal[
    "research_agent", "blog_writer", "linkedin_writer", "image_generator", "content_strategist"
]:
    route = state.get("route", "research")
    route_map = {
        "research": "research_agent",
        "blog": "research_agent",
        "linkedin": "linkedin_writer",
        "image": "image_generator",
        "strategy": "research_agent",
    }
    return route_map.get(route, "research_agent")


def route_after_research(state: dict) -> Literal[
    "blog_writer", "content_strategist", "__end__"
]:
    route = state.get("route", "research")
    if route == "blog":
        return "blog_writer"
    if route == "strategy":
        return "content_strategist"
    return "__end__"
