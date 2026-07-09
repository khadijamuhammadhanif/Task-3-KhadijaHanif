"""
utils.py
Shared helper functions used across the recommendation engine:
JSON persistence, console formatting, and simple input validation.
"""

import json
import os
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
MODELS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models")
VIZ_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "visualizations")


def ensure_dirs():
    """Make sure required directories exist."""
    for d in (DATA_DIR, MODELS_DIR, VIZ_DIR):
        os.makedirs(d, exist_ok=True)


def load_json(path, default=None):
    """Safely load a JSON file, returning `default` if it doesn't exist or is invalid."""
    if not os.path.exists(path):
        return default if default is not None else {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return default if default is not None else {}


def save_json(path, data):
    """Persist a dict/list to disk as pretty-printed JSON."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def clamp(value, low, high):
    return max(low, min(high, value))


def print_header(title, width=64):
    print("\n" + "=" * width)
    print(title.center(width))
    print("=" * width)


def print_divider(width=64):
    print("-" * width)


def validate_rating(raw):
    """Validate a 1-5 star rating input. Returns int or None if invalid."""
    try:
        value = int(raw)
        if 1 <= value <= 5:
            return value
    except (ValueError, TypeError):
        pass
    return None


def validate_menu_choice(raw, valid_choices):
    raw = str(raw).strip()
    return raw if raw in valid_choices else None
