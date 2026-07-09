"""
preprocessing.py
Cleans raw text and builds the combined "feature text" used for
TF-IDF vectorization, for both items and user profiles.
"""

import re


def clean_text(text):
    """Lowercase, strip punctuation, and normalize whitespace."""
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s|]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def tags_to_text(tags_field):
    """Convert a pipe-separated tag string into space-separated tokens,
    repeating each tag so multi-word tags stay intact as single features
    after underscore-joining."""
    if not tags_field:
        return ""
    tags = [t.strip() for t in tags_field.split("|") if t.strip()]
    tokens = [re.sub(r"\s+", "_", t.lower()) for t in tags]
    return " ".join(tokens)


def build_item_corpus(items_df):
    """
    Build the text corpus for each item combining tags (weighted 3x)
    and description, ready for TF-IDF vectorization.
    """
    corpus = []
    for _, row in items_df.iterrows():
        tag_text = tags_to_text(row.get("tags", ""))
        desc_text = clean_text(row.get("description", ""))
        # Tags matter more than free-text description, so repeat them.
        combined = (tag_text + " ") * 3 + desc_text
        corpus.append(combined.strip())
    return corpus


def build_user_text(profile):
    """
    Build a single text representation of a user's profile from their
    genres, categories, interests, skills, and hobbies. Ratings on
    liked items are folded in by the feedback module separately.
    """
    fields = []
    for key in ("favorite_genres", "interests", "skills", "hobbies", "preferred_categories"):
        values = profile.get(key, [])
        if isinstance(values, list):
            fields.extend(values)

    tokens = [re.sub(r"\s+", "_", v.strip().lower()) for v in fields if v and v.strip()]
    return " ".join(tokens)


def parse_natural_language_interests(text):
    """
    Very lightweight NLP-style parser: splits a free-text sentence of
    interests into individual keyword tokens (comma/and/semicolon separated).
    e.g. "I love AI, sci-fi movies and cybersecurity" ->
         ["AI", "sci-fi movies", "cybersecurity"]
    """
    if not text:
        return []
    text = re.sub(r"\bi (love|like|enjoy|prefer)\b", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\band\b", ",", text, flags=re.IGNORECASE)
    parts = re.split(r"[,;/]", text)
    cleaned = [p.strip() for p in parts if p.strip()]
    return cleaned
