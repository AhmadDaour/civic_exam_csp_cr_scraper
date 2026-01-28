import json
import csv
from pathlib import Path
from datetime import datetime, UTC
from scrapers.civique_csp_scraper import CiviqueCSPScraper


RAW_PATH = Path("data/raw/csp_questions_raw.json")
PROCESSED_PATH = Path("data/processed/csp_questions_processed.csv")
PROCESSED_PATH.parent.mkdir(parents=True, exist_ok=True)


# ========================
# SCRAPING
# ========================
scraper = CiviqueCSPScraper()
sections = scraper.run()

payload = {
    "type": "CSP",
    "source_url": scraper.URL,
    "scraped_at": datetime.now(UTC).isoformat(),
    "sections": sections
}

# Save JSON raw
with open(RAW_PATH, "w", encoding="utf-8") as f:
    json.dump(payload, f, indent=2, ensure_ascii=False)

print("✅ JSON raw sauvegardé")


# ========================
# JSON → CSV (FORMAT FINAL)
# ========================

rows = []

for section in payload["sections"]:
    section_title = section.get("section", "").strip().rstrip(":")

    for q in section.get("questions", []):
        # Ici q est une string, pas un dict
        question_text = q.strip()

        rows.append({
            "section": section_title,
            "question": question_text
        })


with open(PROCESSED_PATH, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["section", "question", "source_url"])
    writer.writeheader()
    writer.writerows(rows)

print(f"✅ CSV final sauvegardé : {PROCESSED_PATH}")
print(f"📊 {len(rows)} questions exportées")
