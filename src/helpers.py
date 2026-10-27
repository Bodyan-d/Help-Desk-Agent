import re
from .base_words import STOP_WORDS, SYNONYMS, GENERIC_WORDS

def normalize_text(text: str) -> str:
    text = text.lower()
    text = text.replace("e-bike", "electric bike")

    return text


def tokenize(text: str) -> set[str]:
    text = normalize_text(text)

    words = re.findall(r"[a-z0-9]+", text)

    tokens = set()

    for word in words:
        if word in STOP_WORDS:
            continue

        normalized = SYNONYMS.get(word, word)
        tokens.add(normalized)

    return tokens

def calculate_relevance(
    query_words: set[str],
    section: str,
    heading: str
) -> int:
    section_words = tokenize(section)
    heading_words = tokenize(heading)

    content_matches = query_words & section_words
    heading_matches = query_words & heading_words

    content_score = len(content_matches)

    heading_score = sum(
        1 if word in GENERIC_WORDS else 4
        for word in heading_matches
    )

    return content_score + heading_score