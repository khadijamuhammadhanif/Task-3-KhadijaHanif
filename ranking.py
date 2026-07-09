"""
ranking.py
Combines rule-based and content-based scores into a hybrid ranking,
applies popularity/user-preference weighting, and generates
human-readable explanations for each recommendation.
"""

import numpy as np

# Hybrid weighting: how much each signal contributes to the final score.
WEIGHT_CONTENT = 0.55
WEIGHT_RULE = 0.25
WEIGHT_POPULARITY = 0.10
WEIGHT_RATING = 0.10


def normalize(arr):
    arr = np.asarray(arr, dtype=float)
    if arr.max() == arr.min():
        return np.zeros_like(arr)
    return (arr - arr.min()) / (arr.max() - arr.min())


def compute_hybrid_scores(items_df, content_scores, rule_scores, feedback_adjustment=None):
    """
    Combine content similarity, rule-based overlap, popularity, and
    average rating into a single weighted hybrid score per item.
    `feedback_adjustment` is an optional array of per-item multipliers
    derived from the user's rating history (see feedback.py).
    """
    popularity_norm = normalize(items_df["popularity_score"].values)
    rating_norm = normalize(items_df["rating"].values)

    hybrid = (
        WEIGHT_CONTENT * content_scores
        + WEIGHT_RULE * rule_scores
        + WEIGHT_POPULARITY * popularity_norm
        + WEIGHT_RATING * rating_norm
    )

    if feedback_adjustment is not None:
        hybrid = hybrid * feedback_adjustment

    return hybrid


def rank_items(items_df, hybrid_scores, top_n=10, exclude_ids=None):
    """Return the top-N items sorted by hybrid score, excluding any
    item_ids the user has already seen/rated if requested."""
    df = items_df.copy()
    df["hybrid_score"] = hybrid_scores

    if exclude_ids:
        df = df[~df["item_id"].isin(exclude_ids)]

    df = df.sort_values("hybrid_score", ascending=False).head(top_n)
    return df.reset_index(drop=True)


def explain_recommendation(row, matched_tags, content_score, rule_score):
    """Build a human-readable explanation string for a single recommendation."""
    match_pct = round(row["hybrid_score"] * 100, 1)
    if matched_tags:
        tag_list = ", ".join(t.replace("_", " ").title() for t in matched_tags[:4])
        reason = (
            f"{match_pct}% match. Shares {len(matched_tags)} tag(s) with your interests: {tag_list}."
        )
    else:
        reason = (
            f"{match_pct}% match based on content similarity to your stated preferences "
            f"(popularity and rating also considered)."
        )
    return reason


def confidence_label(hybrid_score):
    """Bonus feature: qualitative confidence score for a recommendation."""
    if hybrid_score >= 0.7:
        return "Very High"
    elif hybrid_score >= 0.5:
        return "High"
    elif hybrid_score >= 0.3:
        return "Moderate"
    else:
        return "Low"
