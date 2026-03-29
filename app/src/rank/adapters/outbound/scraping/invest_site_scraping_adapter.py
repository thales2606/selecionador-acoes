import time

from src.common.constants import URL_INVESTSITE
from src.rank.ports.outbound.Invest_site_scraping_port import InvestSiteScrapingPort
from src.rank.ports.outbound.web_scraping_port import WebScrapingPort


class InvestSiteScrapingAdapter(InvestSiteScrapingPort):
    """Adapter para scraping do site investsite.com.br"""

    # XPaths para filtros
    CHECK_SELECT_ALL = '//*[@id="selectAll"]'
    CHECK_ROI = '//*[@id="itm8"]'
    CHECK_MARGEM_LIQUIDA = '//*[@id="itm11"]'
    CHECK_MARGEM_EBIT = '//*[@id="itm13"]'
    CHECK_EV_EBIT = '//*[@id="itm26"]'
    CHECK_CASH_FLOW_YIELD = '//*[@id="itm29"]'
    CHECK_DY = '//*[@id="itm32"]'
    CHECK_VOLUME_FINANCEIRO = '//*[@id="itm33"]'
    CHECK_MARKET_CAP = '//*[@id="itm34"]'
    INPUT_VOLUME_MINIMO = '//*[@id="tabela_seleciona_acoes"]/tbody/tr[28]/td[2]/input'
    INPUT_MARGEM_EBIT = '//*[@id="tabela_seleciona_acoes"]/tbody/tr[8]/td[2]/input'
    BUTTON_PROCURAR = '//*[@id="form_seleciona_acoes"]/div[1]/div[1]/div/div[1]/button'
    SELECT_QUANTIDADE_ACOES = '//*[@id="stock_screener"]/div/div/div/div[1]/div[1]/label/select'
    TABELA_RESULTADOS = '//*[@id="tabela_selecao_acoes"]'

    # Configurações padrão
    VOLUME_MINIMO = '3000000'
    MARGEM_EBIT_MINIMO = '0'
    QUANTIDADE_POR_PAGINA = '-1'  # Todas as ações

    def __init__(self, web_scraping: WebScrapingPort):
        self._web_scraping = web_scraping

    def apply_filters(self) -> None:
        """Aplica os filtros no site"""
        self._web_scraping.navigate_to(URL_INVESTSITE)
        self._select_all_filters()
        time.sleep(1)
        self._select_all_filters()  # Duplo clique para desselecionar tudo
        time.sleep(1)

        # Seleciona apenas os filtros desejados
        self._select_filter(self.CHECK_ROI)
        self._select_filter(self.CHECK_MARGEM_LIQUIDA)
        self._select_filter(self.CHECK_MARGEM_EBIT)
        self._select_filter(self.CHECK_EV_EBIT)
        self._select_filter(self.CHECK_CASH_FLOW_YIELD)
        self._select_filter(self.CHECK_DY)
        self._select_filter(self.CHECK_VOLUME_FINANCEIRO)
        self._select_filter(self.CHECK_MARKET_CAP)

        # Insere valores nos campos
        self._web_scraping.send_keys_to_element(
            self.INPUT_VOLUME_MINIMO,
            self.VOLUME_MINIMO
        )
        self._web_scraping.send_keys_to_element(
            self.INPUT_MARGEM_EBIT,
            self.MARGEM_EBIT_MINIMO
        )

        # Busca os resultados
        self._web_scraping.click_element(self.BUTTON_PROCURAR)

    def get_results_table(self) -> str:
        """Obtém a tabela de resultados"""
        self._web_scraping.select_dropdown_value(
            self.SELECT_QUANTIDADE_ACOES,
            self.QUANTIDADE_POR_PAGINA
        )
        return self._web_scraping.get_element_html(self.TABELA_RESULTADOS)

    def _select_all_filters(self) -> None:
        """Seleciona/desseleciona todos os filtros"""
        self._web_scraping.click_element(self.CHECK_SELECT_ALL)

    def _select_filter(self, xpath: str) -> None:
        """Seleciona um filtro específico"""
        self._web_scraping.scroll_to_element(xpath)
        time.sleep(0.5)
        self._web_scraping.click_element(xpath)
