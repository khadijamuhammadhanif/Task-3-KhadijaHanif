"""
data_loader.py
Handles loading of the item catalog (CSV) and user profile store (JSON).
"""

import os
import pandas as pd

from src.utils import DATA_DIR, load_json, save_json, ensure_dirs

ITEMS_PATH = os.path.join(DATA_DIR, "items.csv")
USERS_PATH = os.path.join(DATA_DIR, "users.json")


def load_items():
    """Load the item catalog into a pandas DataFrame."""
    ensure_dirs()
    if not os.path.exists(ITEMS_PATH):
        raise FileNotFoundError(
            f"Item dataset not found at {ITEMS_PATH}. Run data/generate_dataset.py first."
        )
    df = pd.read_csv(ITEMS_PATH)
    df["tags"] = df["tags"].fillna("")
    df["description"] = df["description"].fillna("")
    return df


def load_users():
    """Load the full user profile store (all users) as a dict."""
    ensure_dirs()
    return load_json(USERS_PATH, default={})


def save_users(users_dict):
    """Persist the full user profile store back to disk."""
    save_json(USERS_PATH, users_dict)


def get_user(username):
    users = load_users()
    return users.get(username)


def upsert_user(username, profile):
    users = load_users()
    users[username] = profile
    save_users(users)
    return profile
