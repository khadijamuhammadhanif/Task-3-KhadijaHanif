"""
feedback.py
Handles the user rating system, feedback-driven ranking adjustments,
and recommendation history tracking.

Rule: if a user rates an item highly (4-5 stars), items sharing tags
with it get a ranking boost. If rated poorly (1-2 stars), items sharing
tags get a ranking penalty.
"""

import numpy as np

from src.utils import timestamp


def record_rating(profile, item_id, item_name, rating):
    """Append a rating event to the user's history and store it."""
    profile.setdefault("ratings", {})
    profile.setdefault("history", [])

    profile["ratings"][str(item_id)] = rating
    profile["history"].append({
        "item_id": item_id,
        "item_name": item_name,
        "rating": rating,
        "timestamp": timestamp(),
    })
    return profile


def record_recommendation_event(profile, recommended_items):
    """Track what was recommended and when, for history/analytics."""
    profile.setdefault("recommendation_log", [])
    profile["recommendation_log"].append({
        "timestamp": timestamp(),
        "items": [{"item_id": int(i), "item_name": n} for i, n in recommended_items],
    })
    return profile


def compute_feedback_adjustment(items_df, profile):
    """
    Returns a per-item multiplier array (default 1.0) that boosts items
    sharing tags with highly-rated items and penalizes items sharing
    tags with poorly-rated items.
    """
    ratings = profile.get("ratings", {})
    adjustment = np.ones(len(items_df))
    if not ratings:
        return adjustment

    id_to_index = {row["item_id"]: idx for idx, row in items_df.iterrows()}
    id_to_tags = {
        row["item_id"]: {t.strip().lower() for t in str(row["tags"]).split("|") if t.strip()}
        for _, row in items_df.iterrows()
    }

    liked_tags, disliked_tags = set(), set()
    for item_id_str, rating in ratings.items():
        item_id = int(item_id_str)
        tags = id_to_tags.get(item_id, set())
        if rating >= 4:
            liked_tags |= tags
        elif rating <= 2:
            disliked_tags |= tags

    for idx, row in items_df.iterrows():
        item_tags = id_to_tags.get(row["item_id"], set())
        boost = len(item_tags & liked_tags)
        penalty = len(item_tags & disliked_tags)
        # Each shared "liked" tag gives +8%, each shared "disliked" tag gives -12%,
        # clamped to a sane range so scores never go negative or explode.
        multiplier = 1.0 + (0.08 * boost) - (0.12 * penalty)
        adjustment[idx] = max(0.1, min(1.6, multiplier))

    return adjustment


def already_rated_ids(profile):
    return {int(k) for k in profile.get("ratings", {}).keys()}
