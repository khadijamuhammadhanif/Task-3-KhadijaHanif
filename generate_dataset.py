"""
generate_dataset.py
Generates a realistic multi-category dataset of 120 items for the
Intelligent Recommendation Engine (items.csv).

Categories: Movies, Books, Online Courses, Games, Podcasts, Technology Tools
"""

import csv
import random

random.seed(42)

items = []
item_id = 1


def add_item(name, category, tags, description, rating, popularity):
    global item_id
    items.append({
        "item_id": item_id,
        "item_name": name,
        "category": category,
        "tags": tags,  # pipe-separated
        "description": description,
        "rating": rating,
        "popularity_score": popularity,
    })
    item_id += 1


# ---------------------------------------------------------------------
# MOVIES (20)
# ---------------------------------------------------------------------
movies = [
    ("Neon Horizon", "Sci-Fi|Action|Technology|AI", "A rogue AI pilot fights to save a floating city from collapse.", 4.6, 91),
    ("Quiet Static", "Drama|Mystery|Psychological", "A sound engineer uncovers a conspiracy hidden in radio frequencies.", 4.2, 63),
    ("The Last Algorithm", "Sci-Fi|Thriller|AI|Technology", "An engineer races to stop a self-improving algorithm from escaping containment.", 4.7, 95),
    ("Crimson Tide Racing", "Action|Sports|Adventure", "Rival street racers battle for control of the coastal highways.", 4.0, 72),
    ("Whispers of Kyoto", "Drama|Romance|Culture", "Two strangers reconnect over seasons in a quiet Japanese town.", 4.5, 68),
    ("Galaxy Protocol", "Sci-Fi|Space|Adventure|AI", "A starship crew must negotiate with an alien intelligence to survive.", 4.4, 88),
    ("Iron Circuit", "Action|Technology|Superhero", "A disabled engineer builds an exosuit to protect her city.", 4.3, 84),
    ("The Silent Ledger", "Thriller|Crime|Finance", "A forensic accountant unravels a global money-laundering ring.", 4.1, 59),
    ("Paper Lanterns", "Drama|Family|Romance", "A grandmother's letters reveal a hidden wartime love story.", 4.6, 55),
    ("Deep Field", "Sci-Fi|Space|Exploration", "Astronauts discover an anomaly at the edge of the solar system.", 4.5, 80),
    ("Code Red Zero", "Action|Cybersecurity|Thriller", "A hacker must stop a cyberattack on critical infrastructure in real time.", 4.3, 77),
    ("Autumn in Prague", "Romance|Drama|Travel", "Two travelers find unexpected connection during a European gap year.", 4.0, 48),
    ("The Machine Learns", "Sci-Fi|Drama|AI|Technology", "A researcher forms an emotional bond with the AI she trained.", 4.8, 93),
    ("Bhangra Nights", "Comedy|Music|Family", "A wedding DJ tries to save his family's dance academy.", 4.2, 52),
    ("Orbital Decay", "Sci-Fi|Thriller|Space", "A damaged space station crew must survive reentry.", 4.1, 66),
    ("The Startup Wars", "Drama|Business|Technology", "Two co-founders battle over control of their unicorn startup.", 3.9, 61),
    ("Monsoon Diaries", "Drama|Coming-of-Age", "A teenager navigates identity during monsoon season in Kerala.", 4.4, 50),
    ("Firewall", "Thriller|Cybersecurity|Action", "A security analyst discovers she is the target of her own defense system.", 4.2, 70),
    ("Quantum Heist", "Action|Sci-Fi|Heist", "A crew uses quantum computing to pull off an impossible heist.", 4.3, 82),
    ("Sunset Over Lagos", "Drama|Music|Culture", "A struggling musician chases his big break in Lagos' Afrobeat scene.", 4.5, 58),
]
for n, t, d, r, p in movies:
    add_item(n, "Movies", t, d, r, p)

# ---------------------------------------------------------------------
# BOOKS (20)
# ---------------------------------------------------------------------
books = [
    ("Deep Learning Demystified", "AI|Technology|Programming|Data Science", "A beginner-friendly walkthrough of neural networks and deep learning.", 4.7, 89),
    ("The Silent Algorithm", "AI|Fiction|Thriller", "A novel about an AI that predicts crimes before they happen.", 4.3, 65),
    ("Atomic Focus", "Self-Help|Productivity|Psychology", "Practical strategies for building deep focus in a distracted world.", 4.5, 80),
    ("Python for Everyone", "Programming|Technology|Education", "A comprehensive guide to Python for absolute beginners.", 4.6, 92),
    ("Whispering Pines", "Fiction|Mystery|Drama", "A small-town detective uncovers secrets buried for decades.", 4.1, 47),
    ("The Data Science Handbook", "Data Science|AI|Programming|Technology", "Interviews and insights from leading data scientists.", 4.4, 74),
    ("Mindful Leadership", "Business|Self-Help|Psychology", "How mindfulness practices improve executive decision-making.", 4.2, 55),
    ("Neural Networks from Scratch", "AI|Programming|Technology|Data Science", "Build neural networks using only Python and NumPy.", 4.8, 87),
    ("Letters from the Void", "Fiction|Sci-Fi|Space", "An astronaut's letters home during a decade-long deep space mission.", 4.5, 60),
    ("The Lean Startup Playbook", "Business|Technology|Entrepreneurship", "A practical guide to validating startup ideas quickly.", 4.3, 71),
    ("Cosmic Threads", "Fiction|Sci-Fi|Philosophy", "A meditation on consciousness wrapped in a space opera.", 4.4, 58),
    ("Cybersecurity Essentials", "Cybersecurity|Technology|Programming", "A foundational guide to protecting modern systems and networks.", 4.5, 76),
    ("The Art of Habit", "Self-Help|Psychology|Productivity", "How small daily habits compound into major life change.", 4.6, 83),
    ("Recommendation Systems Explained", "AI|Data Science|Programming|Technology", "A practical guide to building recommendation engines from scratch.", 4.7, 85),
    ("Garden of Forgotten Names", "Fiction|Drama|Historical", "A multigenerational saga set across three continents.", 4.3, 52),
    ("Statistics for Machine Learning", "AI|Data Science|Mathematics", "Core statistical foundations behind modern ML algorithms.", 4.4, 69),
    ("The Founder's Dilemma", "Business|Entrepreneurship|Technology", "Real case studies of startup founders navigating hard choices.", 4.1, 57),
    ("Under a Painted Sky", "Fiction|Adventure|Historical", "Two young women disguise themselves to cross the Oregon Trail.", 4.5, 49),
    ("Cloud Computing Fundamentals", "Technology|Cloud|Programming", "An introduction to cloud infrastructure, AWS, and DevOps basics.", 4.3, 73),
    ("The Ethics of AI", "AI|Philosophy|Technology", "A balanced exploration of the moral questions raised by artificial intelligence.", 4.6, 78),
]
for n, t, d, r, p in books:
    add_item(n, "Books", t, d, r, p)

# ---------------------------------------------------------------------
# ONLINE COURSES (20)
# ---------------------------------------------------------------------
courses = [
    ("Machine Learning Specialization", "AI|Data Science|Programming|Technology", "92% match with interests in AI, Data Science, and Programming.", 4.8, 96),
    ("Full-Stack Web Development", "Programming|Technology|Web Development", "Build complete web applications using modern JavaScript frameworks.", 4.5, 88),
    ("Deep Learning with TensorFlow", "AI|Data Science|Programming|Technology", "Hands-on deep learning projects using TensorFlow and Keras.", 4.7, 90),
    ("Data Structures and Algorithms", "Programming|Technology|Computer Science", "Master the core computer science concepts behind coding interviews.", 4.6, 85),
    ("Introduction to Cybersecurity", "Cybersecurity|Technology|Networking", "Learn the fundamentals of network security and ethical hacking.", 4.4, 77),
    ("Cloud Computing with AWS", "Cloud|Technology|DevOps", "Deploy and manage scalable applications on Amazon Web Services.", 4.5, 82),
    ("Python for Data Science", "Programming|Data Science|AI|Technology", "Use Python, Pandas, and NumPy to analyze real-world datasets.", 4.7, 91),
    ("UI/UX Design Fundamentals", "Design|Technology|Creativity", "Learn user-centered design principles for digital products.", 4.3, 68),
    ("Natural Language Processing", "AI|Data Science|Programming|Technology", "Build systems that understand and generate human language.", 4.6, 84),
    ("DevOps and CI/CD Pipelines", "DevOps|Technology|Cloud|Programming", "Automate software delivery using Docker, Kubernetes, and CI/CD.", 4.4, 75),
    ("Game Development with Unity", "Games|Programming|Technology|Design", "Create 2D and 3D games using the Unity engine and C#.", 4.5, 80),
    ("Business Analytics Foundations", "Data Science|Business|Technology", "Use data-driven techniques to inform strategic business decisions.", 4.2, 62),
    ("Blockchain and Web3 Basics", "Technology|Blockchain|Programming", "Understand blockchain fundamentals and smart contract development.", 4.1, 58),
    ("Mobile App Development with Flutter", "Programming|Technology|Mobile", "Build cross-platform mobile apps using Flutter and Dart.", 4.5, 79),
    ("AI Ethics and Governance", "AI|Philosophy|Technology", "Explore responsible AI deployment and governance frameworks.", 4.3, 60),
    ("SQL for Data Analysis", "Data Science|Programming|Technology", "Master relational databases and advanced SQL querying.", 4.6, 83),
    ("Product Management Essentials", "Business|Technology|Strategy", "Learn to lead cross-functional teams and ship successful products.", 4.4, 70),
    ("Computer Vision with OpenCV", "AI|Data Science|Programming|Technology", "Build image recognition and object detection systems.", 4.6, 81),
    ("Digital Marketing Analytics", "Business|Marketing|Data Science", "Use analytics tools to optimize digital marketing campaigns.", 4.0, 54),
    ("Reinforcement Learning Basics", "AI|Data Science|Programming|Technology", "Understand how agents learn optimal behavior through reward signals.", 4.5, 76),
]
for n, t, d, r, p in courses:
    add_item(n, "Online Courses", t, d, r, p)

# ---------------------------------------------------------------------
# GAMES (20)
# ---------------------------------------------------------------------
games = [
    ("Circuit Breach", "Action|Cybersecurity|Technology|Strategy", "Hack through corporate networks in this cyberpunk stealth game.", 4.6, 88),
    ("Starforge Colony", "Sci-Fi|Strategy|Space|Simulation", "Build and manage a self-sustaining colony on a hostile alien world.", 4.5, 84),
    ("Neural Drift", "Sci-Fi|Racing|AI|Technology", "Race AI-controlled vehicles across procedurally generated tracks.", 4.3, 75),
    ("Kingdom of Embers", "Fantasy|RPG|Adventure", "Explore a war-torn fantasy realm as a wandering mercenary.", 4.7, 90),
    ("Puzzle Protocol", "Puzzle|Technology|Strategy", "Solve logic puzzles to reprogram a malfunctioning space station AI.", 4.4, 70),
    ("Shadow Ledger", "Strategy|Crime|Simulation", "Manage a criminal empire while evading a relentless AI detective.", 4.2, 65),
    ("Skybound Legends", "Adventure|Fantasy|Action", "Soar through floating islands as a sky pirate seeking treasure.", 4.5, 79),
    ("Mind Palace", "Puzzle|Psychology|Indie", "Navigate a surreal mindscape to solve emotionally driven puzzles.", 4.6, 68),
    ("Data Miners", "Strategy|Technology|Simulation", "Compete to extract and monetize data in a near-future economy.", 4.1, 58),
    ("Frostbound Tactics", "Strategy|War|Fantasy", "Command armies across icy battlefields in turn-based combat.", 4.4, 73),
    ("Pixel Coders", "Puzzle|Programming|Education", "Learn real coding concepts by solving programming puzzles.", 4.5, 71),
    ("Void Runners", "Sci-Fi|Action|Space|Adventure", "Pilot a starship crew through a collapsing galaxy.", 4.3, 77),
    ("Echoes of Elandra", "RPG|Fantasy|Story-Rich", "An emotionally driven RPG about memory and loss.", 4.7, 82),
    ("Botanica Isles", "Simulation|Relaxation|Nature", "Cultivate a magical island garden ecosystem at your own pace.", 4.6, 66),
    ("Overclock", "Action|Technology|Esports|Strategy", "A fast-paced competitive shooter set in a hyper-connected future.", 4.2, 80),
    ("Chrono Vault", "Puzzle|Sci-Fi|Adventure", "Manipulate time to solve escape-room style challenges.", 4.5, 72),
    ("Iron Frontier", "Strategy|Sci-Fi|Simulation", "Build and defend a mining colony on a resource-rich exoplanet.", 4.3, 69),
    ("Tactical Uplink", "Strategy|Cybersecurity|Technology", "Coordinate a hacker team to infiltrate high-security systems.", 4.4, 74),
    ("Whispering Woods", "Adventure|Fantasy|Indie", "A cozy narrative adventure exploring a mysterious enchanted forest.", 4.6, 63),
    ("Ascendant AI", "Strategy|AI|Technology|Sci-Fi", "Train and evolve your own AI companion to conquer the galaxy.", 4.7, 86),
]
for n, t, d, r, p in games:
    add_item(n, "Games", t, d, r, p)

# ---------------------------------------------------------------------
# PODCASTS (20)
# ---------------------------------------------------------------------
podcasts = [
    ("The AI Frontier", "AI|Technology|Data Science", "Weekly conversations with leading AI researchers and engineers.", 4.7, 87),
    ("Code & Coffee", "Programming|Technology|Career", "Casual deep dives into software engineering practices and career growth.", 4.4, 74),
    ("Mindset Shift", "Self-Help|Psychology|Productivity", "Practical strategies for building resilience and mental clarity.", 4.5, 76),
    ("Startup Signals", "Business|Technology|Entrepreneurship", "Founders share the highs and lows of building companies.", 4.3, 68),
    ("Cyber Uncovered", "Cybersecurity|Technology|Investigations", "Investigative stories from the world of cybercrime and defense.", 4.6, 80),
    ("Data Driven", "Data Science|AI|Programming", "Breaking down real-world machine learning case studies.", 4.5, 78),
    ("The Design Lab", "Design|Technology|Creativity", "Conversations with product designers shaping modern software.", 4.2, 60),
    ("Space Signals", "Space|Science|Exploration", "Exploring the latest discoveries in astronomy and space exploration.", 4.6, 79),
    ("Future of Work", "Business|Technology|Productivity", "How AI and automation are reshaping careers and workplaces.", 4.3, 65),
    ("Philosophy Now", "Philosophy|Psychology|Culture", "Accessible discussions on classic and modern philosophical ideas.", 4.4, 58),
    ("Gaming Uncut", "Games|Technology|Culture", "Honest reviews and interviews from the video game industry.", 4.3, 70),
    ("The Cloud Native Show", "Cloud|DevOps|Technology", "Deep dives into Kubernetes, microservices, and cloud architecture.", 4.4, 66),
    ("History Uncovered", "History|Culture|Education", "Long-form storytelling exploring pivotal moments in world history.", 4.6, 72),
    ("The Ethical Machine", "AI|Philosophy|Technology", "Examining the ethical dilemmas posed by emerging technology.", 4.5, 69),
    ("Indie Hackers Radio", "Business|Technology|Entrepreneurship", "Interviews with solo founders building profitable side projects.", 4.2, 61),
    ("Neural Notes", "AI|Data Science|Technology", "Bite-sized explainers on the latest AI research papers.", 4.5, 73),
    ("Wellness Weekly", "Health|Self-Help|Psychology", "Evidence-based tips for physical and mental well-being.", 4.3, 64),
    ("The Product Mindset", "Business|Technology|Strategy", "Product leaders discuss strategy, roadmaps, and user research.", 4.1, 55),
    ("Quantum Curious", "Science|Technology|Physics", "Making quantum computing and physics approachable for everyone.", 4.4, 62),
    ("Security Sundays", "Cybersecurity|Technology|Networking", "A relaxed weekly roundup of the biggest security news.", 4.2, 59),
]
for n, t, d, r, p in podcasts:
    add_item(n, "Podcasts", t, d, r, p)

# ---------------------------------------------------------------------
# TECHNOLOGY TOOLS (20)
# ---------------------------------------------------------------------
tools = [
    ("VeloCode IDE", "Programming|Technology|Productivity", "A lightweight, extensible code editor with built-in AI autocomplete.", 4.6, 85),
    ("DataForge Analytics", "Data Science|AI|Business", "A drag-and-drop platform for building data pipelines and dashboards.", 4.4, 74),
    ("CloudNest", "Cloud|DevOps|Technology", "A managed cloud hosting platform with one-click deployments.", 4.5, 79),
    ("SecureVault Pro", "Cybersecurity|Technology|Privacy", "Enterprise-grade password and secrets management.", 4.6, 81),
    ("PixelStudio", "Design|Technology|Creativity", "A collaborative design tool for UI/UX prototyping.", 4.3, 68),
    ("ModelHub AI", "AI|Data Science|Programming", "A marketplace and hosting platform for pretrained machine learning models.", 4.7, 88),
    ("TaskFlow", "Productivity|Business|Technology", "A project management tool with automated workflow triggers.", 4.2, 63),
    ("GitStream", "Programming|Technology|DevOps", "A visual Git client that simplifies branching and code review.", 4.4, 70),
    ("InsightBoard", "Data Science|Business|AI", "Real-time analytics dashboards powered by predictive modeling.", 4.5, 76),
    ("ChatBridge API", "AI|Programming|Technology", "An API toolkit for embedding conversational AI into applications.", 4.6, 83),
    ("NetGuard Firewall", "Cybersecurity|Technology|Networking", "A next-generation firewall with AI-based threat detection.", 4.5, 77),
    ("SwiftDeploy CI", "DevOps|Cloud|Technology", "A continuous integration platform with one-click rollback.", 4.3, 66),
    ("VectorBase", "AI|Data Science|Programming", "A vector database optimized for similarity search and embeddings.", 4.7, 84),
    ("FormWise", "Business|Productivity|Technology", "A smart form builder with built-in data validation logic.", 4.1, 54),
    ("CodeReview AI", "Programming|AI|Technology", "An AI-powered assistant for automated code review and refactoring.", 4.6, 82),
    ("EdgeSync", "Cloud|Technology|IoT", "Real-time data synchronization for edge and IoT devices.", 4.2, 60),
    ("MetricLens", "Data Science|Business|Analytics", "A no-code analytics tool for tracking product and marketing KPIs.", 4.3, 65),
    ("AutoMate Studio", "Productivity|Technology|Automation", "Build no-code automation workflows across your favorite apps.", 4.4, 71),
    ("Sentinel Monitor", "Cybersecurity|Technology|DevOps", "Real-time infrastructure monitoring with anomaly detection.", 4.5, 75),
    ("PromptCraft", "AI|Programming|Technology", "A prompt engineering workbench for testing and versioning LLM prompts.", 4.6, 80),
]
for n, t, d, r, p in tools:
    add_item(n, "Technology Tools", t, d, r, p)

# ---------------------------------------------------------------------
# Write to CSV
# ---------------------------------------------------------------------
with open("items.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=["item_id", "item_name", "category", "tags", "description", "rating", "popularity_score"],
    )
    writer.writeheader()
    writer.writerows(items)

print(f"Generated {len(items)} items across {len(set(i['category'] for i in items))} categories -> items.csv")
