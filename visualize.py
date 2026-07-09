"""
visualize.py
Generates the User Preference Dashboard and Recommendation Analytics
charts using matplotlib/seaborn, saved into visualizations/.
"""

import os
import matplotlib
matplotlib.use("Agg")  # headless rendering
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from src.utils import VIZ_DIR, ensure_dirs

sns.set_theme(style="whitegrid")


def plot_user_preferences(profile, save_name="user_preference_dashboard.png"):
    """Bar chart of interest/category distribution for a single user."""
    ensure_dirs()
    fields = {
        "Genres": profile.get("favorite_genres", []),
        "Interests": profile.get("interests", []),
        "Skills": profile.get("skills", []),
        "Hobbies": profile.get("hobbies", []),
        "Categories": profile.get("preferred_categories", []),
    }
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Left: counts per field type
    counts = {k: len(v) for k, v in fields.items() if v}
    if counts:
        axes[0].bar(counts.keys(), counts.values(), color=sns.color_palette("crest", len(counts)))
        axes[0].set_title("Preference Field Distribution")
        axes[0].set_ylabel("Number of Entries")
    else:
        axes[0].text(0.5, 0.5, "No preference data yet", ha="center", va="center")
        axes[0].set_title("Preference Field Distribution")

    # Right: category preferences
    cats = fields["Categories"]
    if cats:
        cat_series = pd.Series(cats).value_counts()
        axes[1].pie(cat_series.values, labels=cat_series.index, autopct="%1.0f%%",
                    colors=sns.color_palette("pastel"))
        axes[1].set_title("Preferred Categories")
    else:
        axes[1].text(0.5, 0.5, "No category preferences set", ha="center", va="center")
        axes[1].set_title("Preferred Categories")

    plt.tight_layout()
    path = os.path.join(VIZ_DIR, save_name)
    plt.savefig(path, dpi=140)
    plt.close(fig)
    return path


def plot_recommendation_analytics(results, save_name="recommendation_analytics.png"):
    """Bar chart of similarity scores + ranking for the current recommendation set."""
    ensure_dirs()
    if not results:
        return None

    df = pd.DataFrame(results)
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    # Left: similarity/match score per item (ranking chart)
    ordered = df.sort_values("match_score", ascending=True)
    axes[0].barh(ordered["item_name"], ordered["match_score"], color=sns.color_palette("flare", len(ordered)))
    axes[0].set_xlabel("Match Score (%)")
    axes[0].set_title("Recommendation Ranking")

    # Right: category breakdown among recommended items
    cat_counts = df["category"].value_counts()
    axes[1].bar(cat_counts.index, cat_counts.values, color=sns.color_palette("crest", len(cat_counts)))
    axes[1].set_title("Popular Categories in Recommendations")
    axes[1].tick_params(axis="x", rotation=30)

    plt.tight_layout()
    path = os.path.join(VIZ_DIR, save_name)
    plt.savefig(path, dpi=140)
    plt.close(fig)
    return path


def plot_similarity_distribution(items_df, content_scores, save_name="similarity_distribution.png"):
    """Histogram of similarity scores across the entire catalog for a user."""
    ensure_dirs()
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(content_scores, bins=20, kde=True, color="#4C72B0", ax=ax)
    ax.set_title("Similarity Score Distribution Across Catalog")
    ax.set_xlabel("Cosine Similarity Score")
    ax.set_ylabel("Number of Items")
    plt.tight_layout()
    path = os.path.join(VIZ_DIR, save_name)
    plt.savefig(path, dpi=140)
    plt.close(fig)
    return path
