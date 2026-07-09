# Intelligent Recommendation Engine Using Artificial Intelligence

A portfolio-ready, GitHub-ready content-based recommendation system that analyzes user
interests, preferences, and behavior to generate personalized, explainable recommendations
— built on the same core principles (TF-IDF + Cosine Similarity) that power Netflix,
Amazon, Spotify, YouTube, and TikTok.

---

## 1. Project Overview

This engine takes a user's stated genres, interests, skills, hobbies, and preferred
categories and recommends the most relevant items from a 120-item catalog spanning six
categories: **Movies, Books, Online Courses, Games, Podcasts, and Technology Tools**.

It combines three recommendation approaches into a single hybrid score:

| Method | What it does |
|---|---|
| **Rule-Based** | Direct tag overlap between user interests and item tags (Jaccard-style) |
| **Content-Based Filtering** | TF-IDF vectorization + Cosine Similarity between user profile and item features |
| **Hybrid** | Weighted combination of rule-based score, content similarity, popularity, and average rating |

Every recommendation includes a **plain-English explanation** of why it was suggested.

---

## 2. Architecture Diagram

```
                     ┌─────────────────────┐
                     │   User Profile /     │
                     │   Interests (Input)  │
                     └──────────┬───────────┘
                                │
                     ┌──────────▼───────────┐
                     │   preprocessing.py    │
                     │  clean + tokenize     │
                     └──────────┬───────────┘
                                │
              ┌─────────────────┼─────────────────┐
              ▼                                     ▼
   ┌────────────────────┐               ┌────────────────────┐
   │   similarity.py     │               │   similarity.py     │
   │  TF-IDF + Cosine     │               │  Rule-based overlap │
   │  (content-based)     │               │  (Jaccard-style)    │
   └──────────┬──────────┘               └──────────┬──────────┘
              │                                       │
              └───────────────────┬───────────────────┘
                                   ▼
                        ┌─────────────────────┐
                        │     feedback.py       │
                        │ rating-based boost/    │
                        │ penalty adjustment     │
                        └──────────┬───────────┘
                                   ▼
                        ┌─────────────────────┐
                        │     ranking.py         │
                        │ hybrid score, sort,     │
                        │ explain, confidence     │
                        └──────────┬───────────┘
                                   ▼
                        ┌─────────────────────┐
                        │   Top-10 Recommen-    │
                        │   dations + Reasons   │
                        └─────────────────────┘
```

## 3. Recommendation Workflow

1. **Collect** user interests (genres, interests, skills, hobbies, categories) — via
   structured input or free-text natural language ("I love AI and sci-fi movies").
2. **Preprocess** input — lowercase, tokenize, normalize.
3. **Vectorize** — build a TF-IDF vector for the user profile in the same vocabulary
   space as the item catalog.
4. **Score** — compute Cosine Similarity (content-based) and tag-overlap (rule-based)
   against every item.
5. **Adjust** — apply feedback-based multipliers from the user's rating history.
6. **Rank** — combine into a hybrid score, sort descending, apply Top-N cutoff.
7. **Explain** — generate a human-readable reason for each recommendation.

---

## 4. Technology Stack

- **Language:** Python 3.12+
- **Libraries:** pandas, numpy, scikit-learn, matplotlib, seaborn, joblib, reportlab

Install everything with:

```bash
pip install -r requirements.txt
```

---

## 5. Project Structure

```
AI-Recommendation-System/
├── data/
│   ├── items.csv              # 120-item catalog across 6 categories
│   ├── users.json             # persisted user profiles, ratings, history
│   └── generate_dataset.py    # regenerates items.csv from scratch
├── models/
│   └── similarity_model.pkl   # persisted TF-IDF vectorizer + item matrix
├── visualizations/
│   ├── user_preference_dashboard.png
│   ├── recommendation_analytics.png
│   └── similarity_distribution.png
├── exports/                   # CSV/PDF exports of recommendations (bonus feature)
├── src/
│   ├── data_loader.py         # load/save items + user profiles
│   ├── preprocessing.py       # text cleaning, vectorization prep, NL parsing
│   ├── similarity.py          # TF-IDF, Cosine Similarity, rule-based scoring
│   ├── ranking.py             # hybrid scoring, sorting, explanations
│   ├── feedback.py            # rating capture + feedback-driven adjustment
│   ├── recommender.py         # RecommendationEngine orchestration class
│   ├── visualize.py           # dashboards and analytics charts
│   ├── evaluation.py          # Precision@K, Recall@K, satisfaction score
│   ├── export.py              # CSV/PDF export
│   └── utils.py                # shared helpers
├── main.py                     # menu-driven CLI application
├── requirements.txt
└── README.md
```

---

## 6. Installation Guide

```bash
# 1. Clone or extract the project
cd AI-Recommendation-System

# 2. (Optional) create a virtual environment
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. (Optional) regenerate the dataset
python3 data/generate_dataset.py

# 5. Run the application
python3 main.py
```

---

## 7. Using the CLI

```
1. Create Profile              -> enter genres, interests, skills, hobbies, categories
2. View Profile                -> see your stored preferences
3. Get Recommendations         -> top 10 personalized items + explanations + charts
4. Rate Recommendations        -> 1-5 star feedback, improves future rankings
5. Update Interests            -> change your profile at any time
6. Save Profile / Model        -> persist preference dashboard + similarity model
7. View Trending Items         -> most popular items catalog-wide
8. Export Recommendations      -> CSV or PDF report
9. Performance Report          -> Precision@K, Recall@K, similarity stats
10. Exit
```

### Sample Output

```
1. Machine Learning Specialization  [Online Courses]  (ID: 41)
   Match: 92.3%   Confidence: Very High   Rating: 4.8/5
   Reason: 92.3% match. Shares 3 tag(s) with your interests: Ai, Data Science, Programming.
```

---

## 8. Similarity Calculation Explained

1. **Feature extraction** — each item's tags (weighted 3x) and description are combined
   into a single text document; the same is done for the user profile.
2. **TF-IDF weighting** — Term Frequency rewards terms that appear often within an item;
   Inverse Document Frequency penalizes terms that appear across most items (e.g. generic
   words), so specific/descriptive tags carry more weight.
3. **Cosine Similarity** — measures the angle between the user vector and each item
   vector, which is invariant to profile/description length — two vectors pointing in
   the same direction score close to 1, orthogonal vectors score close to 0.
4. **Rule-based overlap** — a simpler Jaccard-style score used alongside cosine similarity
   as a sanity-check signal and to power tag-based explanations.
5. **Hybrid formula:**

```
hybrid_score = 0.55 * content_similarity
             + 0.25 * rule_based_overlap
             + 0.10 * normalized_popularity
             + 0.10 * normalized_rating
```
   This score is then multiplied by a feedback adjustment factor derived from the user's
   rating history (see below).

---

## 9. Feedback Learning

- Rating an item **4-5 stars** boosts the ranking of other items sharing its tags
  (+8% per shared tag).
- Rating an item **1-2 stars** reduces the ranking of other items sharing its tags
  (-12% per shared tag).
- Adjustments are clamped to a `[0.1, 1.6]` multiplier range to keep scores stable.

---

## 10. Evaluation Metrics

Available via CLI option 9 (`Performance Report`):

- **Precision@K** — fraction of the top-K recommendations that are relevant (rating ≥ 4.5)
- **Recall@K** — fraction of all relevant items captured in the top-K
- **User Satisfaction Score** — average of the user's given star ratings, normalized to 0-1
- **Similarity Distribution** — mean/median/std/min/max cosine similarity across the
  full catalog for the current user

> Note: in the absence of external ground-truth labels, "relevant" items are approximated
> as catalog items with rating ≥ 4.5 among the recommended set. In a production system,
> relevance would be derived from actual user click-through/purchase/watch data.

---

## 11. Bonus Features Implemented

- ✅ Collaborative-filtering-style rating feedback loop (tag-based boost/penalty)
- ✅ Recommendation Confidence Score (Very High / High / Moderate / Low)
- ✅ Multi-category recommendations in a single ranked list
- ✅ Trending Item Detection (by popularity score)
- ✅ Natural Language Preference Input ("I love AI and cybersecurity" → parsed interests)
- ✅ Recommendation Export to CSV/PDF
- ✅ Basic User Segmentation (by dominant preferred category)
- ✅ Model persistence via Joblib (TF-IDF vectorizer + item matrix)

---

## 12. Dataset Description

`data/items.csv` contains 120 items (20 per category) with the following fields:

| Column | Description |
|---|---|
| `item_id` | Unique integer ID |
| `item_name` | Display name |
| `category` | One of: Movies, Books, Online Courses, Games, Podcasts, Technology Tools |
| `tags` | Pipe-separated tags (e.g. `AI\|Technology\|Programming`) |
| `description` | Short free-text description |
| `rating` | Average rating (1-5) |
| `popularity_score` | Popularity index (0-100) |

Regenerate anytime with `python3 data/generate_dataset.py`.

---

## 13. Screenshots Section

Run the app and choose option 3 (Get Recommendations) or option 6 (Save Profile) to
generate the following charts in `visualizations/`:

- `user_preference_dashboard.png` — interest field distribution + category pie chart
- `recommendation_analytics.png` — ranking bar chart + category breakdown of results
- `similarity_distribution.png` — histogram of cosine similarity across the full catalog

---

## 14. GitHub Deployment Guide

```bash
git init
git add .
git commit -m "Initial commit: Intelligent Recommendation Engine"
git branch -M main
git remote add origin <your-repo-url>
git push -u origin main
```

Suggested `.gitignore`:
```
__pycache__/
*.pyc
venv/
exports/
models/*.pkl
```

---

## 15. Limitations & Future Work

- **Cold Start:** brand-new users with no interests produce zero-score vectors; the
  Trending Items view (option 7) can be used as a fallback.
- **Collaborative Filtering:** this project is intentionally content-based only. A
  true collaborative-filtering layer would require historical multi-user interaction
  data, which is out of scope here but is a natural extension (`src/similarity.py`
  can be extended with a user-item interaction matrix).
- **NLP Parsing:** the natural-language interest parser is intentionally lightweight
  (comma/and-splitting), not a full NER/embedding pipeline.

---

## License

Built for educational/portfolio purposes.
