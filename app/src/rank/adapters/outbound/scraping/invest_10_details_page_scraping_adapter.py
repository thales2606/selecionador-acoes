import time

from src.common.constants import URL_INVEST10_DETAILS
from src.rank.ports.outbound.details_page_scraping_port import DetailsPageScrapingPort
from src.rank.ports.outbound.web_scraping_port import WebScrapingPort


class Invest10DetailsPageScrapingAdapter(DetailsPageScrapingPort):
    LABEL_LUCRO_LIQUIDO = '//*[@id="table-balance-results"]/tbody/tr[5]/td[2]/div[2]'
    LABEL_PATRIMONIO_LIQUIDO = '/html/body/div[4]/div[2]/main/section/div/div[5]/div[3]/div[2]/div/div[3]/span[2]/div[2]'
    LABEL_TAX = '//*[@id="table-balance-results"]/tbody/tr[8]/td[2]/div[2]'

    def __init__(self, web_scraping: WebScrapingPort):
        self._web_scraping = web_scraping
        self._banner_has_close = False

    def scrape_details_page(self, stock_code: str, financial: bool) -> dict:
        self._web_scraping.navigate_to(URL_INVEST10_DETAILS + stock_code + "/")
        time.sleep(0.5)
        self._close_banner()
        self._contabil_value_datails()
        return {
            'patrimonio_liquido': self._get_patrimonio_liquido(),
            'lucro_liquido_anual': self._get_lucro_liquido(True),
            'imposto_anual': self._get_tax(stock_code),
            'lucro_liquido_trimestral': self._get_lucro_liquido(False),
            'imposto_trimestral': self._get_tax(stock_code)
        }

    def _close_banner(self):
        try:
            if self._banner_has_close:
                return
            time.sleep(30)
            close_button_xpath = '//*[@id="guest-user-banner-irpf"]/div[2]/div/div/button'
            self._web_scraping.click_element(close_button_xpath)
            time.sleep(0.5)
            self._banner_has_close = True
        except Exception as e:
            print(f"Erro ao fechar banner: {e}")

    def _get_lucro_liquido(self, yearly=True):
        try:
            self._contabil_period(yearly)
            self._contabil_value_datails()
            return self._web_scraping.get_element_text(self.LABEL_LUCRO_LIQUIDO)
        except Exception as e:
            print(f"Erro ao obter lucro líquido: {e}")
            return ""

    def _get_patrimonio_liquido(self):
        try:
            select2_selector_xpath = "//span[@role='textbox' and contains(@id, 'select2-company-values-view')]"
            self._web_scraping.scroll_to_element(select2_selector_xpath)
            time.sleep(1)
            self._web_scraping.click_element(select2_selector_xpath)
            time.sleep(1)
            option_xpath = "//li[@role='option' and contains(@id, 'detail-value')]"
            self._web_scraping.click_element(option_xpath)
            time.sleep(1)
            return self._web_scraping.get_element_text(self.LABEL_PATRIMONIO_LIQUIDO)
        except Exception as e:
            print(f"Erro ao obter patrimônio líquido: {e}")
            return ""

    def _get_tax(self, stock_code):
        try:
            tax_element = self._web_scraping.get_element_text(
                '//*[@id="table-balance-results"]/tbody/tr[8]/td[2]/div[2]')
            return tax_element
        except Exception as e:
            print(f"Erro ao determinar imposto: {e}")
            return "Desconhecida"

    def _contabil_value_datails(self):
        try:
            self._contabil_value_simple()
            select2_selector_xpath = "//span[@role='textbox' and contains(@id, 'select2-balance-results-values-view')]"
            self._web_scraping.scroll_to_element(select2_selector_xpath)
            self._web_scraping.click_element(select2_selector_xpath)
            option_xpath = "//li[@role='option' and contains(@id, 'detail-value')]"
            self._web_scraping.click_element(option_xpath)
        except Exception as e:
            print(f"Erro ao selecionar valor detalhado: {e}")

    def _contabil_value_simple(self):
        try:
            select2_selector_xpath = "//span[@role='textbox' and contains(@id, 'select2-balance-results-values-view')]"
            self._web_scraping.scroll_to_element(select2_selector_xpath)
            self._web_scraping.click_element(select2_selector_xpath)
            option_xpath = "//li[@role='option' and contains(@id, 'simple-value')]"
            self._web_scraping.click_element(option_xpath)
        except Exception as e:
            print(f"Erro ao selecionar valor simples: {e}")

    def _contabil_period(self, yearly=False):
        try:
            select2_selector_xpath = "//span[@role='textbox' and contains(@id, 'select2-balance-results-category')]"
            self._web_scraping.scroll_to_element(select2_selector_xpath)
            time.sleep(0.5)
            self._web_scraping.click_element(select2_selector_xpath)
            time.sleep(0.5)
            option_xpath = "//li[@role='option' and contains(@id, 'quarter')]"
            if yearly:
                option_xpath = "//li[@role='option' and contains(@id, 'yearly')]"
            self._web_scraping.click_element(option_xpath)
            time.sleep(0.5)
        except Exception as e:
            print(f"Erro ao selecionar período contábil: {e}")
