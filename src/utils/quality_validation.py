import re


_CONTENT_SPECS = {
    "blog": {
        "min_words": 800,
        "max_words": 2000,
        "required_elements": ["#", "##"],
        "name": "Blog Post",
    },
    "linkedin": {
        "min_words": 50,
        "max_words": 500,
        "required_elements": ["#"],  # hashtag
        "name": "LinkedIn Post",
    },
    "research": {
        "min_words": 300,
        "max_words": 5000,
        "required_elements": [],
        "name": "Research Report",
    },
    "strategy": {
        "min_words": 400,
        "max_words": 5000,
        "required_elements": ["##"],
        "name": "Content Strategy",
    },
}


def validate_content(content: str, content_type: str) -> dict:
    spec = _CONTENT_SPECS.get(content_type, _CONTENT_SPECS["research"])
    word_count = len(content.split())
    issues = []
    suggestions = []
    score = 100

    # Length check
    if word_count < spec["min_words"]:
        deficit = spec["min_words"] - word_count
        issues.append(f"Too short: {word_count} words (need {spec['min_words']}+)")
        suggestions.append(f"Add {deficit} more words to meet minimum length.")
        score -= 30
    elif word_count > spec["max_words"]:
        issues.append(f"Too long: {word_count} words (max {spec['max_words']})")
        suggestions.append("Consider trimming or splitting into multiple pieces.")
        score -= 10

    # Structure checks for blog
    if content_type == "blog":
        if not re.search(r"^#\s", content, re.MULTILINE):
            issues.append("Missing H1 title (# Title)")
            suggestions.append("Add a compelling H1 title at the top.")
            score -= 15
        h2_count = len(re.findall(r"^##\s", content, re.MULTILINE))
        if h2_count < 2:
            issues.append(f"Only {h2_count} H2 sections (need 2+)")
            suggestions.append("Add more section headers for better structure.")
            score -= 10

    # LinkedIn specific checks
    if content_type == "linkedin":
        if "#" not in content:
            issues.append("No hashtags found")
            suggestions.append("Add 3-5 relevant hashtags at the end.")
            score -= 15
        if len(content) > 3000:
            issues.append(f"Post too long ({len(content)} chars, LinkedIn max is 3000)")
            suggestions.append("Shorten the post to under 3000 characters.")
            score -= 20

    # Readability: check for very long sentences
    sentences = re.split(r"[.!?]+", content)
    long_sentences = [s for s in sentences if len(s.split()) > 40]
    if long_sentences:
        suggestions.append(f"Break up {len(long_sentences)} long sentence(s) for readability.")
        score -= 5 * len(long_sentences)

    score = max(0, score)
    return {
        "score": score,
        "word_count": word_count,
        "issues": issues,
        "suggestions": suggestions,
        "passed": score >= 60,
    }
