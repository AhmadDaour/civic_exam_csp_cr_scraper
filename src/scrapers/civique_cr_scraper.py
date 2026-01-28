from scrapers.civique_base_scraper import CiviqueBaseQuestionsScraper


class CiviqueCRScraper(CiviqueBaseQuestionsScraper):
    URL = (
        "https://formation-civique.interieur.gouv.fr/"
        "examen-civique/liste-officielle-des-questions-de-connaissance-cr/"
    )
