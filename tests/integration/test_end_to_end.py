"""
Integration tests — these make real API calls and require valid API keys in .env.
Run with: pytest tests/integration/ -v -m integration
"""
import pytest


@pytest.mark.integration
def test_full_linkedin_workflow():
    """Test the full pipeline for a LinkedIn post request."""
    from src.core.workflow import app

    initial_state = {
        "messages": [{"role": "user", "content": "Write a LinkedIn post about the importance of lifelong learning"}],
        "route": "", "topic": "", "audience": "professionals", "tone": "inspirational",
        "research_data": "", "content_output": "", "image_url": None,
        "seo_metadata": {}, "quality_score": {}, "error": None,
    }

    result = app.invoke(initial_state, config={"configurable": {"thread_id": "test-linkedin"}})

    assert result["route"] == "linkedin"
    assert len(result["content_output"]) > 50
    assert "#" in result["content_output"]


@pytest.mark.integration
def test_full_research_workflow():
    """Test the full pipeline for a research request."""
    from src.core.workflow import app

    initial_state = {
        "messages": [{"role": "user", "content": "Research the latest trends in generative AI"}],
        "route": "", "topic": "", "audience": "tech professionals", "tone": "technical",
        "research_data": "", "content_output": "", "image_url": None,
        "seo_metadata": {}, "quality_score": {}, "error": None,
    }

    result = app.invoke(initial_state, config={"configurable": {"thread_id": "test-research"}})

    assert result["route"] == "research"
    assert len(result["content_output"]) > 200
    assert result["error"] is None
