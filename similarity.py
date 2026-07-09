"""
similarity.py
Core similarity math: TF-IDF vectorization + cosine similarity
(content-based filtering), and a simple rule-based tag-overlap score.
"""

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.preprocessing import build_item_corpus, build_user_text


class SimilarityEngine:
    """
    Wraps a fitted TF-IDF vectorizer over the item corpus and exposes
    methods to score a user profile against every item.
    """

    def __init__(self, items_df):
        self.items_df = items_df.reset_index(drop=True)
        self.corpus = build_item_corpus(self.items_df)
        self.vectorizer = TfidfVectorizer()
        self.item_matrix = self.vectorizer.fit_transform(self.corpus)

    # ------------------------------------------------------------------
    # Content-based filtering (TF-IDF + Cosine Similarity)
    # ------------------------------------------------------------------
    def content_similarity(self, profile):
        """Return a numpy array of cosine similarity scores (0-1) between
        the user profile and every item in the catalog."""
        user_text = build_user_text(profile)
        if not user_text.strip():
            return np.zeros(len(self.items_df))
        user_vector = self.vectorizer.transform([user_text])
        scores = cosine_similarity(user_vector, self.item_matrix).flatten()
        return scores

    # ------------------------------------------------------------------
    # Rule-based filtering (direct tag overlap / Jaccard-style)
    # ------------------------------------------------------------------
    def rule_based_score(self, profile):
        """Return a numpy array of matching-percentage scores (0-1) based
        on direct overlap between user interests and item tags."""
        user_terms = set()
        for key in ("favorite_genres", "interests", "skills", "hobbies", "preferred_categories"):
            for v in profile.get(key, []):
                if v:
                    user_terms.add(v.strip().lower())

        scores = np.zeros(len(self.items_df))
        if not user_terms:
            return scores

        for i, tags_field in enumerate(self.items_df["tags"]):
            item_tags = {t.strip().lower() for t in str(tags_field).split("|") if t.strip()}
            if not item_tags:
                continue
            overlap = user_terms.intersection(item_tags)
            union = user_terms.union(item_tags)
            scores[i] = len(overlap) / len(union) if union else 0.0
        return scores

    def matched_tags(self, profile, item_row):
        user_terms = set()
        for key in ("favorite_genres", "interests", "skills", "hobbies", "preferred_categories"):
            for v in profile.get(key, []):
                if v:
                    user_terms.add(v.strip().lower())
        item_tags = {t.strip().lower() for t in str(item_row.get("tags", "")).split("|") if t.strip()}
        return sorted(user_terms.intersection(item_tags))
