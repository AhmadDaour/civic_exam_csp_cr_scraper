from scrapers.civique_base_scraper import CiviqueBaseQuestionsScraper


class CiviqueCSPScraper(CiviqueBaseQuestionsScraper):
    URL = (
        "https://formation-civique.interieur.gouv.fr/"
        "examen-civique/liste-officielle-des-questions-de-connaissance-csp/"
    )
