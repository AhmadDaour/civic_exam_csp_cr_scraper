import requests
from bs4 import BeautifulSoup
from abc import ABC


class CiviqueBaseQuestionsScraper(ABC):
    URL: str = None

    def fetch_page(self) -> str:
        if not self.URL:
            raise ValueError("URL must be defined")

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

        # Parcours du HTML dans l'ordre (clé de la logique)
        for element in soup.find_all(["b", "li"]):

            # SECTION
            if element.name == "b":
                title = element.get_text(strip=True)

                if title.endswith(":"):
                    current_section = {
                        "section": title.replace(" :", ":").strip(),
                        "questions": []
                    }
                    sections.append(current_section)

            # QUESTION
            elif (
                element.name == "li"
                and element.has_attr("data-block-key")
                and current_section
            ):
                question = element.get_text(strip=True)
                if question:
                    current_section["questions"].append(question)

        return [s for s in sections if s["questions"]]

    def run(self):
        html = self.fetch_page()
        return self.parse(html)
