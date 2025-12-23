import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime


class CiviqueCSPScraper:
    URL = (
        "https://formation-civique.interieur.gouv.fr/"
        "examen-civique/liste-officielle-des-questions-de-connaissance-csp/"
    )

    def fetch_page(self) -> str:
        response = requests.get(
            self.URL,
            timeout=20,
            headers={
                "User-Agent": "Mozilla/5.0 (compatible; CivicScraper/1.0)"
            }
        )
        response.raise_for_status()
        return response.text

    def parse(self, html: str):
        soup = BeautifulSoup(html, "html.parser")

        sections = []
        current_section = None

        # On parcourt le contenu dans l'ordre du HTML
        for element in soup.find_all(["b", "li"]):

            # SECTION : <b>...</b>
            if element.name == "b":
                title = element.get_text(strip=True)

                # On garde uniquement les vrais titres
                if title.endswith(":"):
                    current_section = {
                        "section": title.replace(" :", ":").strip(),
                        "questions": []
                    }
                    sections.append(current_section)

            # QUESTION : <li data-block-key="...">
            elif (
                element.name == "li"
                and element.has_attr("data-block-key")
                and current_section
            ):
                question = element.get_text(strip=True)
                if question:
                    current_section["questions"].append(question)

        # Nettoyage : retirer sections sans questions
        sections = [s for s in sections if s["questions"]]

        return sections

    def run(self):
        html = self.fetch_page()
        return self.parse(html)


if __name__ == "__main__":
    scraper = CiviqueCSPScraper()
    data = scraper.run()

    output_path = "data/raw/csp_questions_raw.json"

    payload = {
        "source_url": scraper.URL,
        "scraped_at": datetime.utcnow().isoformat(),
        "sections": data
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    print(
        f"Scraping completed: {len(data)} sections "
        f"saved to {output_path}"
    )
