"""
export.py
Bonus feature: export a set of recommendations to CSV or a simple PDF report.
"""

import csv
import os
from datetime import datetime

from src.utils import VIZ_DIR, ensure_dirs

EXPORT_DIR = os.path.join(os.path.dirname(VIZ_DIR), "exports")


def export_to_csv(username, results, filename=None):
    ensure_dirs()
    os.makedirs(EXPORT_DIR, exist_ok=True)
    filename = filename or f"{username}_recommendations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    path = os.path.join(EXPORT_DIR, filename)

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "item_id", "item_name", "category", "match_score",
            "confidence", "rating", "popularity_score", "explanation",
        ])
        writer.writeheader()
        for r in results:
            writer.writerow({k: r[k] for k in writer.fieldnames})
    return path


def export_to_pdf(username, results, filename=None):
    """Simple text-based PDF export using reportlab if available,
    otherwise falls back to a plain-text .txt report."""
    ensure_dirs()
    os.makedirs(EXPORT_DIR, exist_ok=True)
    filename = filename or f"{username}_recommendations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    path = os.path.join(EXPORT_DIR, filename)

    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas

        c = canvas.Canvas(path, pagesize=letter)
        width, height = letter
        y = height - 50
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y, f"Recommendations for {username}")
        y -= 30
        c.setFont("Helvetica", 10)
        for r in results:
            line = f"{r['item_name']} ({r['category']}) - {r['match_score']}% match"
            c.drawString(50, y, line)
            y -= 15
            c.drawString(60, y, r["explanation"][:100])
            y -= 20
            if y < 60:
                c.showPage()
                y = height - 50
        c.save()
        return path
    except ImportError:
        # Fallback: plain text report with .pdf-like naming avoided
        txt_path = path.replace(".pdf", ".txt")
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(f"Recommendations for {username}\n")
            f.write("=" * 50 + "\n")
            for r in results:
                f.write(f"{r['item_name']} ({r['category']}) - {r['match_score']}% match\n")
                f.write(f"  {r['explanation']}\n\n")
        return txt_path
