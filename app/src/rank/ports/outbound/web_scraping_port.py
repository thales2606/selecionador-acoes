from abc import ABC, abstractmethod


class WebScrapingPort(ABC):
    """Interface para adaptadores de web scraping"""

    @abstractmethod
    def navigate_to(self, url: str) -> None:
        """Navega para uma URL"""
        pass

    @abstractmethod
    def click_element(self, xpath: str) -> None:
        """Clica em um elemento"""
        pass

    @abstractmethod
    def get_element_html(self, xpath: str) -> str:
        """Obtém o HTML de um elemento"""
        pass

    @abstractmethod
    def get_element_text(self, xpath: str) -> str:
        """Obtém o HTML de um elemento"""
        pass

    @abstractmethod
    def select_dropdown_value(self, xpath: str, value: str) -> None:
        """Seleciona um valor em um dropdown"""
        pass

    @abstractmethod
    def scroll_to_element(self, xpath: str) -> None:
        """Faz scroll até um elemento"""
        pass

    @abstractmethod
    def send_keys_to_element(self, xpath: str, keys: str) -> None:
        """Envia texto para um elemento"""
        pass

    @abstractmethod
    def close(self) -> None:
        """Fecha o navegador"""
        pass
