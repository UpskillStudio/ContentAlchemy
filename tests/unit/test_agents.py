import json
import pytest
from unittest.mock import patch, MagicMock


class TestQueryHandler:
    def test_routes_blog_request(self):
        mock_response = json.dumps({
            "route": "blog",
            "topic": "remote work productivity",
            "audience": "managers",
            "tone": "professional",
        })
        with patch("src.agents.query_handler.create_message", return_value=mock_response):
            from src.agents.query_handler import run_query_handler
            state = {"messages": [{"role": "user", "content": "Write a blog about remote work"}]}
            result = run_query_handler(state)
            assert result["route"] == "blog"
            assert result["topic"] == "remote work productivity"

    def test_routes_linkedin_request(self):
        mock_response = json.dumps({
            "route": "linkedin",
            "topic": "AI leadership",
            "audience": "executives",
            "tone": "inspirational",
        })
        with patch("src.agents.query_handler.create_message", return_value=mock_response):
            from src.agents.query_handler import run_query_handler
            state = {"messages": [{"role": "user", "content": "LinkedIn post about AI leadership"}]}
            result = run_query_handler(state)
            assert result["route"] == "linkedin"

    def test_handles_invalid_json_gracefully(self):
        with patch("src.agents.query_handler.create_message", return_value="not valid json"):
            from src.agents.query_handler import run_query_handler
            state = {"messages": [{"role": "user", "content": "some request"}]}
            result = run_query_handler(state)
            assert result["route"] == "research"  # fallback
            assert result["error"] is not None

    def test_handles_empty_messages(self):
        from src.agents.query_handler import run_query_handler
        result = run_query_handler({"messages": []})
        assert result["error"] is not None


class TestResearchAgent:
    def test_returns_research_data(self):
        mock_search = [{"title": "AI Trends", "url": "http://example.com", "content": "AI is growing fast."}]
        mock_synthesis = "## Research Report\n\nAI is transforming industries rapidly."

        with patch("src.integrations.tavily_client.search", return_value=mock_search), \
             patch("src.agents.research_agent.create_message", return_value=mock_synthesis):
            from src.agents.research_agent import run_research_agent
            state = {"topic": "AI trends 2025", "tone": "professional"}
            result = run_research_agent(state)
            assert result["research_data"] == mock_synthesis
            assert result["error"] is None

    def test_handles_tavily_failure(self):
        with patch("src.integrations.tavily_client.search", side_effect=Exception("API timeout")):
            from src.agents.research_agent import run_research_agent
            state = {"topic": "AI trends", "tone": "professional"}
            result = run_research_agent(state)
            assert result["error"] is not None
            assert "research_data" in result


class TestLinkedInWriter:
    def test_generates_post_with_hashtags(self):
        mock_post = "AI is reshaping how we work.\n\nHere are 3 things I learned this week...\n\n#AI #Leadership #Innovation #Technology #FutureOfWork"
        with patch("src.agents.linkedin_writer.create_message", return_value=mock_post):
            from src.agents.linkedin_writer import run_linkedin_writer
            state = {"topic": "AI trends", "audience": "professionals", "tone": "professional", "research_data": ""}
            result = run_linkedin_writer(state)
            assert "#" in result["content_output"]
            assert result["error"] is None


class TestBlogWriter:
    def test_generates_blog_with_seo_data(self):
        mock_blog = "# Remote Work Productivity Guide\n\n## Introduction\nRemote work has transformed...\n\n## Key Strategies\n- Strategy 1\n- Strategy 2\n\n## Conclusion\nIn summary..."
        with patch("src.agents.blog_writer.create_message", return_value=mock_blog):
            from src.agents.blog_writer import run_blog_writer
            state = {
                "topic": "remote work productivity",
                "audience": "managers",
                "tone": "professional",
                "research_data": "Research shows 70% of remote workers are more productive.",
            }
            result = run_blog_writer(state)
            assert result["content_output"] == mock_blog
            assert "seo_metadata" in result
            assert "quality_score" in result
