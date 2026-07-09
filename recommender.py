"""
recommender.py
The RecommendationEngine class orchestrates data loading, similarity
scoring, ranking, feedback adjustment, and explanation generation into
a single, easy-to-use interface for the CLI (main.py) and evaluation
scripts.
"""

import os
import joblib

from src.data_loader import load_items, get_user, upsert_user
from src.similarity import SimilarityEngine
from src.ranking import compute_hybrid_scores, rank_items, explain_recommendation, confidence_label
from src.feedback import (
    compute_feedback_adjustment,
    record_rating,
    record_recommendation_event,
    already_rated_ids,
)
from src.utils import MODELS_DIR, ensure_dirs


class RecommendationEngine:
    def __init__(self):
        ensure_dirs()
        self.items_df = load_items()
        self.sim_engine = SimilarityEngine(self.items_df)

    # ------------------------------------------------------------------
    # Profile management
    # ------------------------------------------------------------------
    def create_or_update_profile(self, username, favorite_genres=None, interests=None,
                                  skills=None, hobbies=None, preferred_categories=None):
        profile = get_user(username) or {
            "username": username,
            "ratings": {},
            "history": [],
            "recommendation_log": [],
        }
        if favorite_genres is not None:
            profile["favorite_genres"] = favorite_genres
        if interests is not None:
            profile["interests"] = interests
        if skills is not None:
            profile["skills"] = skills
        if hobbies is not None:
            profile["hobbies"] = hobbies
        if preferred_categories is not None:
            profile["preferred_categories"] = preferred_categories

        upsert_user(username, profile)
        return profile

    def get_profile(self, username):
        return get_user(username)

    # ------------------------------------------------------------------
    # Recommendation generation
    # ------------------------------------------------------------------
    def recommend(self, username, top_n=10, exclude_rated=True):
        profile = get_user(username)
        if not profile:
            raise ValueError(f"No profile found for user '{username}'.")

        content_scores = self.sim_engine.content_similarity(profile)
        rule_scores = self.sim_engine.rule_based_score(profile)
        feedback_adj = compute_feedback_adjustment(self.items_df, profile)

        hybrid_scores = compute_hybrid_scores(self.items_df, content_scores, rule_scores, feedback_adj)

        exclude_ids = already_rated_ids(profile) if exclude_rated else None
        ranked_df = rank_items(self.items_df, hybrid_scores, top_n=top_n, exclude_ids=exclude_ids)

        results = []
        for _, row in ranked_df.iterrows():
            idx = self.items_df.index[self.items_df["item_id"] == row["item_id"]][0]
            matched = self.sim_engine.matched_tags(profile, row)
            reason = explain_recommendation(row, matched, content_scores[idx], rule_scores[idx])
            results.append({
                "item_id": int(row["item_id"]),
                "item_name": row["item_name"],
                "category": row["category"],
                "tags": row["tags"],
                "description": row["description"],
                "rating": float(row["rating"]),
                "popularity_score": float(row["popularity_score"]),
                "match_score": round(float(row["hybrid_score"]) * 100, 1),
                "confidence": confidence_label(row["hybrid_score"]),
                "explanation": reason,
            })

        record_recommendation_event(profile, [(r["item_id"], r["item_name"]) for r in results])
        upsert_user(username, profile)
        return results

    # ------------------------------------------------------------------
    # Feedback
    # ------------------------------------------------------------------
    def rate_item(self, username, item_id, rating):
        profile = get_user(username)
        if not profile:
            raise ValueError(f"No profile found for user '{username}'.")
        item_row = self.items_df[self.items_df["item_id"] == int(item_id)]
        if item_row.empty:
            raise ValueError(f"Item id {item_id} not found.")
        item_name = item_row.iloc[0]["item_name"]
        record_rating(profile, int(item_id), item_name, rating)
        upsert_user(username, profile)
        return profile

    # ------------------------------------------------------------------
    # Persistence (bonus: model persistence)
    # ------------------------------------------------------------------
    def save_similarity_model(self, filename="similarity_model.pkl"):
        path = os.path.join(MODELS_DIR, filename)
        joblib.dump({
            "vectorizer": self.sim_engine.vectorizer,
            "item_matrix": self.sim_engine.item_matrix,
            "item_ids": self.items_df["item_id"].tolist(),
        }, path)
        return path

    def trending_items(self, top_n=5):
        """Bonus: trending item detection based on popularity_score."""
        return self.items_df.sort_values("popularity_score", ascending=False).head(top_n)

    def user_segment(self, username):
        """Bonus: simple user segmentation based on dominant preferred category."""
        profile = get_user(username)
        if not profile:
            return "Unknown"
        cats = profile.get("preferred_categories", [])
        if not cats:
            return "General / Unsegmented"
        return f"{cats[0]} Enthusiast"
