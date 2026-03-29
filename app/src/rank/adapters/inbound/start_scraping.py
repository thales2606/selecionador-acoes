from src.rank.ports.inbound.find_Stoks_use_case_port import FindStoksUseCasePort


class StartScrapingController:
    """Controlador para orquestrar o process de scraping de ações"""

    def __init__(self, use_case: FindStoksUseCasePort):
        self._use_case = use_case

    def start_scraping(self):
        self._use_case.execute()
