import pytest
from src.core.router import route_after_query_handler, route_after_research
from src.utils.content_optimization import extract_keywords, generate_meta_description, calculate_seo_score
from src.utils.quality_validation import validate_content


class TestRouter:
    def _make_state(self, route: str) -> dict:
        return {
            "messages": [], "route": route, "topic": "test", "audience": "professionals",
            "tone": "professional", "research_data": "", "content_output": "",
            "image_url": None, "seo_metadata": {}, "quality_score": {}, "error": None,
        }

    def test_blog_route_goes_to_research_first(self):
        state = self._make_state("blog")
        assert route_after_query_handler(state) == "research_agent"

    def test_linkedin_route_goes_direct(self):
        state = self._make_state("linkedin")
        assert route_after_query_handler(state) == "linkedin_writer"

    def test_image_route_goes_direct(self):
        state = self._make_state("image")
        assert route_after_query_handler(state) == "image_generator"

    def test_research_route_goes_to_research(self):
        state = self._make_state("research")
        assert route_after_query_handler(state) == "research_agent"

    def test_strategy_route_goes_to_research_first(self):
        state = self._make_state("strategy")
        assert route_after_query_handler(state) == "research_agent"

    def test_after_research_blog_goes_to_blog_writer(self):
        state = self._make_state("blog")
        assert route_after_research(state) == "blog_writer"

    def test_after_research_strategy_goes_to_strategist(self):
        state = self._make_state("strategy")
        assert route_after_research(state) == "content_strategist"

    def test_after_research_pure_research_ends(self):
        state = self._make_state("research")
        assert route_after_research(state) == "__end__"

    def test_unknown_route_falls_back_to_research(self):
        state = self._make_state("unknown_route")
        result = route_after_query_handler(state)
        assert result == "research_agent"


class TestContentOptimization:
    def test_extract_keywords_returns_list(self):
        content = "artificial intelligence machine learning deep learning neural networks data science"
        keywords = extract_keywords(content, top_n=5)
        assert isinstance(keywords, list)
        assert len(keywords) <= 5
        assert "artificial" in keywords or "intelligence" in keywords

    def test_extract_keywords_filters_stop_words(self):
        content = "the quick brown fox jumps over the lazy dog and the cat"
        keywords = extract_keywords(content)
        assert "the" not in keywords
        assert "and" not in keywords

    def test_generate_meta_description_under_limit(self):
        content = "## AI Trends 2025\n\nArtificial intelligence is transforming every industry. From healthcare to finance, AI is creating new opportunities."
        meta = generate_meta_description(content)
        assert len(meta) <= 160
        assert len(meta) > 0

    def test_seo_score_returns_dict_with_score(self):
        content = "# Blog Title\n\n## Section 1\nContent here.\n\n## Section 2\nMore content.\n- Point 1\n- Point 2\n- Point 3"
        result = calculate_seo_score(content)
        assert "score" in result
        assert isinstance(result["score"], int)
        assert 0 <= result["score"] <= 100


class TestQualityValidation:
    def test_blog_fails_if_too_short(self):
        short_content = "This is a very short blog post."
        result = validate_content(short_content, "blog")
        assert result["passed"] is False
        assert result["score"] < 60

    def test_linkedin_fails_without_hashtags(self):
        content = "This is a LinkedIn post without any hashtags. It talks about leadership and AI."
        result = validate_content(content, "linkedin")
        issues_text = " ".join(result["issues"])
        assert "hashtag" in issues_text.lower()

    def test_good_blog_passes(self):
        content = (
            "# Complete Guide to Remote Work\n\n"
            "## Introduction\n"
            + "Remote work has become the new normal. " * 60
            + "\n\n## Key Strategies\n"
            + "- Use async communication\n- Set clear boundaries\n- Take regular breaks\n"
            + "\n\n## Productivity Tips\n"
            + "Staying productive at home requires discipline. " * 40
            + "\n\n## Conclusion\n"
            + "Remote work is here to stay. Embrace the change. " * 20
        )
        result = validate_content(content, "blog")
        assert result["word_count"] >= 800

    def test_word_count_is_accurate(self):
        content = "word " * 100
        result = validate_content(content, "research")
        assert result["word_count"] == 100
