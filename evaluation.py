"""
evaluation.py
Computes evaluation metrics for the recommendation engine: Precision@K,
Recall@K, average user satisfaction (from ratings), and similarity
distribution stats. Produces a text performance report.
"""

import numpy as np


def precision_at_k(recommended_ids, relevant_ids, k):
    """Fraction of the top-K recommended items that are relevant."""
    top_k = recommended_ids[:k]
    if not top_k:
        return 0.0
    hits = len(set(top_k) & set(relevant_ids))
    return hits / len(top_k)


def recall_at_k(recommended_ids, relevant_ids, k):
    """Fraction of all relevant items captured in the top-K recommendations."""
    if not relevant_ids:
        return 0.0
    top_k = recommended_ids[:k]
    hits = len(set(top_k) & set(relevant_ids))
    return hits / len(relevant_ids)


def user_satisfaction_score(profile):
    """Average star rating (normalized to 0-1) across a user's rating history."""
    ratings = profile.get("ratings", {})
    if not ratings:
        return None
    values = list(ratings.values())
    return round(sum(values) / (len(values) * 5), 3)


def similarity_distribution_stats(content_scores):
    scores = np.asarray(content_scores, dtype=float)
    return {
        "mean": round(float(scores.mean()), 4),
        "std": round(float(scores.std()), 4),
        "min": round(float(scores.min()), 4),
        "max": round(float(scores.max()), 4),
        "median": round(float(np.median(scores)), 4),
    }


def build_performance_report(profile, recommended_ids, relevant_ids, content_scores, k=10):
    """Assemble a full evaluation report as a formatted string."""
    p_at_k = precision_at_k(recommended_ids, relevant_ids, k)
    r_at_k = recall_at_k(recommended_ids, relevant_ids, k)
    satisfaction = user_satisfaction_score(profile)
    sim_stats = similarity_distribution_stats(content_scores)

    lines = [
        "PERFORMANCE REPORT",
        "=" * 50,
        f"Precision@{k}: {p_at_k:.3f}",
        f"Recall@{k}:    {r_at_k:.3f}",
        f"User Satisfaction Score: {satisfaction if satisfaction is not None else 'N/A (no ratings yet)'}",
        "",
        "Similarity Score Distribution (across full catalog):",
        f"  Mean:   {sim_stats['mean']}",
        f"  Median: {sim_stats['median']}",
        f"  Std:    {sim_stats['std']}",
        f"  Min:    {sim_stats['min']}",
        f"  Max:    {sim_stats['max']}",
    ]
    return "\n".join(lines)
