import json
import hashlib
import pandas as pd
from pathlib import Path


RAW_PATH = Path("data/raw/csp_questions_raw.json")
OUTPUT_PATH = Path("data/processed/csp_questions.csv")


def load_raw_data():
    if not RAW_PATH.exists():
        raise FileNotFoundError(f"{RAW_PATH} not found")

    with open(RAW_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def transform_to_dataframe(raw_data: dict) -> pd.DataFrame:
    rows = []

    source_url = raw_data.get("source_url")
    scraped_at = raw_data.get("scraped_at")

    for section in raw_data.get("sections", []):
        section_title = section.get("section")

        for question in section.get("questions", []):
            rows.append(
                {
                    "section": section_title,
                    "question": question,
                    "source_url": source_url
                }
            )

    df = pd.DataFrame(rows)

    # Nettoyage léger
    df["section"] = df["section"].str.strip()
    df["question"] = df["question"].str.strip()

    return df


def save_csv(df: pd.DataFrame):
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8")
    print(f"CSV generated: {OUTPUT_PATH} ({len(df)} rows)")


def file_hash(path):
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

if __name__ == "__main__":
    raw_data = load_raw_data()
    df = transform_to_dataframe(raw_data)
    save_csv(df)
