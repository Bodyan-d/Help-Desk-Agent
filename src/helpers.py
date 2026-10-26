import re
from base_words import STOP_WORDS, SYNONYMS

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