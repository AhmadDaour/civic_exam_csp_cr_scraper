import json
import sys
import hashlib

from pathlib import Path
from datetime import datetime

# --------------------
# PATH SETUP
# --------------------
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from scrapers.civique_csp_scraper import CiviqueCSPScraper
from pipelines.transform_to_csv import (
    load_raw_data,
    transform_to_dataframe,
    save_csv
)

# --------------------
# CONSTANTS
# --------------------
RAW_PATH = Path("data/raw/csp_questions_raw.json")
CSV_PATH = Path("data/processed/csp_questions.csv")


# --------------------
# UTILS
# --------------------
def file_hash(path: Path) -> str:
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


# --------------------
# PIPELINE STEPS
# --------------------
def run_scraping():
    print("▶ Starting scraping...")
    scraper = CiviqueCSPScraper()
    sections = scraper.run()

    payload = {
        "source_url": scraper.URL,
        "scraped_at": datetime.utcnow().isoformat(),
        "sections": sections,
    }

    RAW_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(RAW_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    print(f"✔ Scraping completed ({len(sections)} sections)")


def run_transformation():
    print("▶ Starting transformation to CSV...")
    raw_data = load_raw_data()
    df = transform_to_dataframe(raw_data)
    save_csv(df)
    print("✔ CSV generation completed")


# --------------------
# MAIN
# --------------------
def main():
    print("🚀 Starting CSP pipeline")

    # 1️⃣ Hash du CSV existant (s'il existe)
    old_hash = None
    if CSV_PATH.exists():
        old_hash = file_hash(CSV_PATH)

    # 2️⃣ Scraping
    run_scraping()

    # 3️⃣ CSV Transformation
    run_transformation()

    # 4️⃣ New CSV Hash  
    new_hash = file_hash(CSV_PATH)

    # 5️⃣ CSV comparison
    if old_hash == new_hash:
        print("🟡 No changes detected in CSV")
    else:
        print("🟢 CSV updated")

    print("✅ Pipeline executed successfully")


if __name__ == "__main__":
    main()
