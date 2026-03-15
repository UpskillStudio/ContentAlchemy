import re
from collections import Counter


_STOP_WORDS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "is", "are", "was", "were", "be", "been",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "that", "this", "these", "those", "it", "its",
    "we", "our", "you", "your", "they", "their", "he", "she", "i", "my",
    "as", "if", "so", "not", "no", "up", "out", "about", "into", "than",
    "more", "all", "also", "can", "just", "which", "when", "there",
}


def extract_keywords(content: str, top_n: int = 10) -> list[str]:
    words = re.findall(r"\b[a-zA-Z]{4,}\b", content.lower())
    filtered = [w for w in words if w not in _STOP_WORDS]
    counts = Counter(filtered)
    return [word for word, _ in counts.most_common(top_n)]


def generate_meta_description(content: str, max_length: int = 160) -> str:
    # Strip markdown headers and symbols
    clean = re.sub(r"#+\s*", "", content)
    clean = re.sub(r"\*+", "", clean)
    clean = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", clean)
    clean = re.sub(r"\s+", " ", clean).strip()

    # Take first meaningful sentence(s) up to max_length
    sentences = re.split(r"(?<=[.!?])\s+", clean)
    description = ""
    for sentence in sentences:
        if len(description) + len(sentence) + 1 <= max_length:
            description += (" " if description else "") + sentence
        else:
            break

    if not description:
        description = clean[:max_length]

    return description.strip()


def calculate_seo_score(content: str) -> dict:
    score = 0
    details = {}
    word_count = len(content.split())

    # Word count check (800-1500 is ideal)
    if 800 <= word_count <= 1500:
        score += 25
        details["word_count"] = f"{word_count} words (optimal)"
    elif 500 <= word_count < 800:
        score += 15
        details["word_count"] = f"{word_count} words (below optimal, aim for 800+)"
    else:
        score += 5
        details["word_count"] = f"{word_count} words (too short or too long)"

    # H2 headers present
    h2_count = len(re.findall(r"^##\s", content, re.MULTILINE))
    if h2_count >= 3:
        score += 20
        details["headers"] = f"{h2_count} H2 headers (good structure)"
    elif h2_count >= 1:
        score += 10
        details["headers"] = f"{h2_count} H2 headers (add more)"
    else:
        details["headers"] = "No H2 headers found"

    # Bullet points / lists
    list_count = len(re.findall(r"^[-*]\s", content, re.MULTILINE))
    if list_count >= 5:
        score += 15
        details["lists"] = f"{list_count} list items (scannable)"
    elif list_count >= 1:
        score += 8
        details["lists"] = f"{list_count} list items"
    else:
        details["lists"] = "No lists found"

    # Links / references
    link_count = len(re.findall(r"\[.+?\]\(.+?\)", content))
    if link_count >= 2:
        score += 10
        details["links"] = f"{link_count} links"
    else:
        details["links"] = "No links found (add references)"

    # Paragraph structure (short paragraphs are better)
    paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
    long_paras = sum(1 for p in paragraphs if len(p.split()) > 80)
    if long_paras == 0:
        score += 15
        details["paragraphs"] = "Good paragraph length"
    else:
        score += 5
        details["paragraphs"] = f"{long_paras} paragraphs are too long (split them up)"

    # Meta description marker present
    if "meta description" in content.lower() or len(content) > 500:
        score += 15
        details["meta"] = "Content ready for meta description"

    return {"score": min(score, 100), "details": details}
