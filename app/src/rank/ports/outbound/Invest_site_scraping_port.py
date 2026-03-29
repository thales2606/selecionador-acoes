from abc import ABC, abstractmethod


class InvestSiteScrapingPort(ABC):
    """Abstract adapter para scraping do site investsite.com.br"""

    @abstractmethod
    def apply_filters(self) -> None:
        pass

    @abstractmethod
    def get_results_table(self) -> str:
        pass
