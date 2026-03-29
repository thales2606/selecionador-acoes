import time

from src.common.constants import URL_INVESTSITE_DETAILS
from src.rank.ports.outbound.details_page_scraping_port import DetailsPageScrapingPort
from src.rank.ports.outbound.web_scraping_port import WebScrapingPort


class InvestSiteDetailsPageScrapingAdapter(DetailsPageScrapingPort):
    """Adapter para scraping da página de detalhes do site investsite.com.br"""

    LABEL_LUCRO_LIQUIDO_ANUAL = '//*[@id="tabela_resumo_empresa_dre_12meses_tbody"]/tr[6]/td[2]/a'
    LABEL_LUCRO_LIQUIDO_TRIMESTRE = '//*[@id="tabela_resumo_empresa_dre_3meses_tbody"]/tr[6]/td[2]/a'
    LABEL_PATRIMONIO_LIQUIDO = '//*[@id="tabela_resumo_empresa_bp_tbody"]/tr[7]/td[2]/a'
    LABEL_SITUACAO_EMPRESA = '//*[@id="tabela_resumo_empresa"]/tbody/tr[4]/td[2]'

    def __init__(self, web_scraping: WebScrapingPort):
        self._web_scraping = web_scraping

    def scrape_details_page(self, stock_code: str):
        self._web_scraping.navigate_to(URL_INVESTSITE_DETAILS + stock_code)
        time.sleep(1)
        return {
            'lucro_liquido_anual': self._get_lucro_liquido_anual(),
            'lucro_liquido_trimestral': self._get_lucro_liquido_trimestral(),
            'patrimonio_liquido': self._get_patrimonio_liquido(),
            'situacao_empresa': self._get_situacao_empresa()
        }
    def _get_lucro_liquido_anual(self):
        try:
            return self._web_scraping.get_element_text(self.LABEL_LUCRO_LIQUIDO_ANUAL)
        except Exception as e:
            print(f"Erro ao obter lucro líquido anual: {e}")
            return None
    def _get_lucro_liquido_trimestral(self):
        try:
            return self._web_scraping.get_element_text(self.LABEL_LUCRO_LIQUIDO_TRIMESTRE)
        except Exception as e:
            print(f"Erro ao obter lucro líquido trimestral: {e}")
            return None
    def _get_patrimonio_liquido(self):
        try:
            return self._web_scraping.get_element_text(self.LABEL_PATRIMONIO_LIQUIDO)
        except Exception as e:
            print(f"Erro ao obter patrimônio líquido: {e}")
            return None
    def _get_situacao_empresa(self):
        try:
            return self._web_scraping.get_element_text(self.LABEL_SITUACAO_EMPRESA)
        except Exception as e:
            print(f"Erro ao obter situação da empresa: {e}")
            return None