import time

from src.common.constants import URL_INVESTSITE, URL_INVESTSITE_FINANCEIRAS
from src.rank.ports.outbound.Invest_site_scraping_port import InvestSiteScrapingPort
from src.rank.ports.outbound.web_scraping_port import WebScrapingPort


class InvestSiteFinancialScrapingAdapter(InvestSiteScrapingPort):
    """Adapter para scraping de ações financeiras do site investsite.com.br"""

    # XPaths para filtros de ações financeiras
    CHECK_MARGEM_LIQUIDA = '//*[@id="itm9"]'
    CHECK_DY = '//*[@id="itm19"]'
    CHECK_VOLUME_FINANCEIRO = '//*[@id="itm20"]'
    CHECK_MARKET_CAP = '//*[@id="itm21"]'

    # XPaths para inputs de valores
    INPUT_VOLUME_MINIMO = '//*[@id="tabela_seleciona_acoes"]/tbody/tr[15]/td[2]/input'
    BUTTON_PROCURAR = '//*[@id="form_seleciona_acoes"]/div[1]/div[1]/div/div[1]/button'
    SELECT_QUANTIDADE_ACOES = '//*[@id="stock_screener_financ"]/div/div/div/div[1]/div[1]/label/select'
    TABELA_RESULTADOS = '//*[@id="tabela_selecao_acoes"]'

    # Configurações padrão
    VOLUME_MINIMO = '3000000'
    QUANTIDADE_POR_PAGINA = '-1'  # Todas as ações
    CHECK_SELECT_ALL = '//*[@id="selectAll"]'

    def __init__(self, web_scraping: WebScrapingPort):
        self._web_scraping = web_scraping

    def apply_filters(self) -> None:
        self._web_scraping.navigate_to(URL_INVESTSITE_FINANCEIRAS)
        self._select_all_filters()
        time.sleep(1)
        self._select_all_filters()  # Duplo clique para desselecionar tudo
        time.sleep(1)

        self._select_filter(self.CHECK_MARGEM_LIQUIDA)
        self._select_filter(self.CHECK_DY)
        self._select_filter(self.CHECK_VOLUME_FINANCEIRO)
        self._select_filter(self.CHECK_MARKET_CAP)

        # Insere valor de volume mínimo
        self._web_scraping.send_keys_to_element(
            self.INPUT_VOLUME_MINIMO,
            self.VOLUME_MINIMO
        )

        # Busca os resultados
        self._web_scraping.click_element(self.BUTTON_PROCURAR)

    def get_results_table(self) -> str:
        """Obtém a tabela de resultados"""
        try:
            self._web_scraping.select_dropdown_value(
                self.SELECT_QUANTIDADE_ACOES,
                self.QUANTIDADE_POR_PAGINA
            )
        except:
            # Se não conseguir selecionar a quantidade, continua mesmo assim
            pass

        return self._web_scraping.get_element_html(self.TABELA_RESULTADOS)

    def _select_filter(self, xpath: str) -> None:
        """Seleciona um filtro específico"""
        self._web_scraping.scroll_to_element(xpath)
        time.sleep(0.5)
        self._web_scraping.click_element(xpath)

    def _select_all_filters(self) -> None:
        """Seleciona/desseleciona todos os filtros"""
        self._web_scraping.click_element(self.CHECK_SELECT_ALL)
