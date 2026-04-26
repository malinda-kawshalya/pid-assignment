import re


def clean_text(text: str) -> str:
    """Normalize incoming review text for prediction."""
    if not text:
        return ""

    text = text.lower().strip()
    text = re.sub(r"http\S+|www\S+", " ", text)
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text
