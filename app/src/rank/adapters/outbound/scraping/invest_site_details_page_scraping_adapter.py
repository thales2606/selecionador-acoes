import time

from src.common.constants import URL_INVESTSITE_DETAILS, URL_INVEST10_DETAILS
from src.rank.ports.outbound.details_page_scraping_port import DetailsPageScrapingPort
from src.rank.ports.outbound.web_scraping_port import WebScrapingPort


class InvestSiteDetailsPageScrapingAdapter(DetailsPageScrapingPort):
    LABEL_SITUACAO_EMPRESA = '//*[@id="tabela_resumo_empresa"]/tbody/tr[4]/td[2]'
    def __init__(self, web_scraping: WebScrapingPort):
        self._web_scraping = web_scraping

    def scrape_details_page(self, stock_code: str, financial: bool) -> dict:
        self._web_scraping.navigate_to(URL_INVESTSITE_DETAILS + stock_code)
        time.sleep(1)
        return {
            'situacao_empresa': self._get_situacao_empresa(),
        }
    def _get_situacao_empresa(self):
        try:
            return self._web_scraping.get_element_text(self.LABEL_SITUACAO_EMPRESA)
        except Exception as e:
            print(f"Erro ao obter situação da empresa: {e}")
            return ""
