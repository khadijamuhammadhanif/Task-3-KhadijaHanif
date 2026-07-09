"""
main.py
Menu-driven CLI application for the Intelligent Recommendation Engine.

Run with:  python3 main.py
"""

import sys

from src.recommender import RecommendationEngine
from src.preprocessing import parse_natural_language_interests
from src.visualize import plot_user_preferences, plot_recommendation_analytics, plot_similarity_distribution
from src.evaluation import build_performance_report
from src.export import export_to_csv, export_to_pdf
from src.utils import print_header, print_divider, validate_rating, validate_menu_choice


MENU = """
1. Create Profile
2. View Profile
3. Get Recommendations
4. Rate Recommendations
5. Update Interests
6. Save Profile / Model
7. View Trending Items
8. Export Last Recommendations (CSV/PDF)
9. Performance Report
10. Exit
"""


def prompt_list(label):
    raw = input(f"{label} (comma-separated, or press Enter to skip): ").strip()
    if not raw:
        return []
    return [item.strip() for item in raw.split(",") if item.strip()]


def create_profile(engine):
    print_header("CREATE PROFILE")
    username = input("Enter username: ").strip()
    if not username:
        print("Username cannot be empty.")
        return None

    print("\nTell us about yourself. You can also just describe your interests in a sentence.")
    nl_text = input("Describe your interests in your own words (optional): ").strip()
    nl_interests = parse_natural_language_interests(nl_text)

    genres = prompt_list("Favorite genres")
    interests = prompt_list("Interests") + nl_interests
    skills = prompt_list("Skills")
    hobbies = prompt_list("Hobbies")
    categories = prompt_list("Preferred categories (e.g. Movies, Books, Games)")

    profile = engine.create_or_update_profile(
        username,
        favorite_genres=genres,
        interests=interests,
        skills=skills,
        hobbies=hobbies,
        preferred_categories=categories,
    )
    print(f"\nProfile created/updated for '{username}'.")
    return username


def view_profile(engine, username):
    profile = engine.get_profile(username)
    if not profile:
        print("No profile found. Create one first.")
        return
    print_header(f"PROFILE: {username}")
    for key in ("favorite_genres", "interests", "skills", "hobbies", "preferred_categories"):
        print(f"  {key.replace('_', ' ').title()}: {', '.join(profile.get(key, [])) or '(none)'}")
    print(f"  Ratings given: {len(profile.get('ratings', {}))}")
    print(f"  Recommendation events: {len(profile.get('recommendation_log', []))}")
    print(f"  Segment: {engine.user_segment(username)}")


def get_recommendations(engine, username):
    profile = engine.get_profile(username)
    if not profile:
        print("No profile found. Create one first.")
        return None
    try:
        results = engine.recommend(username, top_n=10)
    except ValueError as e:
        print(f"Error: {e}")
        return None

    if not results:
        print("No recommendations could be generated. Try adding more interests.")
        return None

    print_header(f"TOP {len(results)} RECOMMENDATIONS FOR {username}")
    for i, r in enumerate(results, start=1):
        print(f"\n{i}. {r['item_name']}  [{r['category']}]  (ID: {r['item_id']})")
        print(f"   Match: {r['match_score']}%   Confidence: {r['confidence']}   Rating: {r['rating']}/5")
        print(f"   Reason: {r['explanation']}")
    print_divider()

    content_scores = engine.sim_engine.content_similarity(profile)
    plot_recommendation_analytics(results)
    plot_similarity_distribution(engine.items_df, content_scores)
    print("Charts saved to visualizations/ (recommendation_analytics.png, similarity_distribution.png)")

    return results


def rate_recommendations(engine, username, last_results):
    profile = engine.get_profile(username)
    if not profile:
        print("No profile found. Create one first.")
        return
    if not last_results:
        print("Get recommendations first before rating them.")
        return

    print_header("RATE RECOMMENDATIONS")
    for r in last_results:
        raw = input(f"Rate '{r['item_name']}' 1-5 stars (Enter to skip): ").strip()
        if not raw:
            continue
        rating = validate_rating(raw)
        if rating is None:
            print("  Invalid rating, skipped.")
            continue
        engine.rate_item(username, r["item_id"], rating)
        print(f"  Recorded {rating} stars for '{r['item_name']}'.")
    print("\nFeedback recorded. Future recommendations will reflect your ratings.")


def update_interests(engine, username):
    profile = engine.get_profile(username)
    if not profile:
        print("No profile found. Create one first.")
        return
    print_header("UPDATE INTERESTS")
    print("Leave blank to keep existing values.")
    new_genres = prompt_list("New favorite genres")
    new_interests = prompt_list("New interests")
    new_categories = prompt_list("New preferred categories")

    engine.create_or_update_profile(
        username,
        favorite_genres=(new_genres or profile.get("favorite_genres")),
        interests=(new_interests or profile.get("interests")),
        preferred_categories=(new_categories or profile.get("preferred_categories")),
    )
    print("Interests updated.")


def save_profile(engine, username):
    profile = engine.get_profile(username)
    if profile:
        plot_user_preferences(profile)
        print("User preference dashboard saved to visualizations/user_preference_dashboard.png")
    path = engine.save_similarity_model()
    print(f"Similarity model persisted to {path}")
    print("User profiles are auto-saved to data/users.json on every change.")


def view_trending(engine):
    print_header("TRENDING ITEMS")
    trending = engine.trending_items(top_n=5)
    for _, row in trending.iterrows():
        print(f"  {row['item_name']} [{row['category']}] - Popularity: {row['popularity_score']}")


def export_recommendations(username, last_results):
    if not last_results:
        print("Get recommendations first.")
        return
    fmt = input("Export as (csv/pdf): ").strip().lower()
    if fmt == "csv":
        path = export_to_csv(username, last_results)
    else:
        path = export_to_pdf(username, last_results)
    print(f"Exported to {path}")


def performance_report(engine, username):
    profile = engine.get_profile(username)
    if not profile:
        print("No profile found. Create one first.")
        return
    content_scores = engine.sim_engine.content_similarity(profile)
    results = engine.recommend(username, top_n=10, exclude_rated=False)
    recommended_ids = [r["item_id"] for r in results]
    # "Relevant" items approximated as those with rating >= 4.5 among recommended set,
    # standing in for ground-truth relevance in absence of external labels.
    relevant_ids = [r["item_id"] for r in results if r["rating"] >= 4.5]

    report = build_performance_report(profile, recommended_ids, relevant_ids, content_scores, k=10)
    print_header("PERFORMANCE REPORT")
    print(report)


def main():
    engine = RecommendationEngine()
    current_user = None
    last_results = None

    print_header("INTELLIGENT RECOMMENDATION ENGINE")
    print(f"Loaded {len(engine.items_df)} items across "
          f"{engine.items_df['category'].nunique()} categories.")

    while True:
        print(MENU)
        choice = input("Select an option (1-10): ").strip()

        if choice == "1":
            current_user = create_profile(engine) or current_user

        elif choice == "2":
            if not current_user:
                current_user = input("Enter username to view: ").strip()
            view_profile(engine, current_user)

        elif choice == "3":
            if not current_user:
                current_user = input("Enter username: ").strip()
            last_results = get_recommendations(engine, current_user)

        elif choice == "4":
            rate_recommendations(engine, current_user, last_results)

        elif choice == "5":
            update_interests(engine, current_user)

        elif choice == "6":
            save_profile(engine, current_user)

        elif choice == "7":
            view_trending(engine)

        elif choice == "8":
            export_recommendations(current_user, last_results)

        elif choice == "9":
            performance_report(engine, current_user)

        elif choice == "10":
            print("Goodbye!")
            sys.exit(0)

        else:
            print("Invalid choice. Please select 1-10.")


if __name__ == "__main__":
    main()
