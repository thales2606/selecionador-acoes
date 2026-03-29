from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select
from src.rank.ports.outbound.web_scraping_port import WebScrapingPort


class WebScrapingDriver(WebScrapingPort):
    """Adapter para WebDriver com Selenium"""

    def __init__(self):
        self.driver = None
        self._initialize_driver()

    def _initialize_driver(self) -> None:
        """Inicializa o WebDriver Firefox"""
        options = Options()
        options.headless = True
        self.driver = webdriver.Firefox(options=options)

    def navigate_to(self, url: str) -> None:
        """Navega para uma URL"""
        self.driver.get(url)

    def click_element(self, xpath: str) -> None:
        """Clica em um elemento"""
        self.driver.find_element(by=By.XPATH, value=xpath).click()

    def get_element_html(self, xpath: str) -> str:
        """Obtém o HTML de um elemento"""
        return self.driver.find_element(by=By.XPATH, value=xpath).get_attribute('outerHTML')

    def get_element_text(self, xpath: str) -> str:
        """Obtém o texto de um elemento"""
        return self.driver.find_element(by=By.XPATH, value=xpath).text

    def select_dropdown_value(self, xpath: str, value: str) -> None:
        """Seleciona um valor em um dropdown"""
        element = self.driver.find_element(by=By.XPATH, value=xpath)
        select = Select(element)
        select.select_by_value(value)

    def scroll_to_element(self, xpath: str) -> None:
        """Faz scroll até um elemento"""
        element = self.driver.find_element(by=By.XPATH, value=xpath)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
            element
        )

    def send_keys_to_element(self, xpath: str, keys: str) -> None:
        """Envia texto para um elemento"""
        self.driver.find_element(by=By.XPATH, value=xpath).send_keys(keys)

    def close(self) -> None:
        """Fecha o navegador"""
        if self.driver:
            self.driver.quit()

    def __del__(self):
        """Garante que o driver seja fechado ao destruir o objeto"""
        self.close()
