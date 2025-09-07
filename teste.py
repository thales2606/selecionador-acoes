import json
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver


class WebScraping:

    def __init__(self, url, remote_url='http://localhost:4444/wd/hub'):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        self.drive: WebDriver = webdriver.Remote(
            command_executor=remote_url,
            options=chrome_options
        )

        if url:
            self.drive.get(url)

    def get_element_by_xpath(self, xPath):
        return self.drive.find_element(by=By.XPATH, value=xPath)

    def click(self, xPath):
        self.get_element_by_xpath(xPath).click()

    def scroll_to_element(self, xPath):
        elemento = self.get_element_by_xpath(xPath)
        self.drive.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", elemento)

    def get_outerhtml(self, xPath):
        return self.get_element_by_xpath(xPath).get_attribute("outerHTML")

    def get_innerhtml(self, xPath):
        return self.get_element_by_xpath(xPath).get_attribute("innerHTML")

    def finalizar(self):
        self.drive.quit()


def executar_scraping(parametros_json: str):
    dados = json.loads(parametros_json)
    scraping = WebScraping(url=dados.get("url"))

    resultados = []

    for acao in dados.get("acoes", []):
        tipo = acao.get("acao")
        xpath = acao.get("xpath")

        if tipo == "click":
            scraping.click(xpath)
        elif tipo == "scroll":
            scraping.scroll_to_element(xpath)
        elif tipo == "extrair_outerhtml":
            conteudo = scraping.get_outerhtml(xpath)
            resultados.append({"xpath": xpath, "conteudo": conteudo})
        elif tipo == "extrair_innerhtml":
            conteudo = scraping.get_innerhtml(xpath)
            resultados.append({"xpath": xpath, "conteudo": conteudo})

    scraping.finalizar()
    return json.dumps(resultados, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    # O JSON será passado como primeiro argumento na execução via linha de comando
    query = {
        "url":"https://exemplo.com",
        "acoes":        [
            {
                "acao":"scroll",
                "xpath":"//div[@id='area']"
            },
            {
                "acao":"click",
                "xpath":"//button[@id='botao']"
            },
            {
                "acao":"extrair_outerhtml",
                "xpath":"//div[@id='conteudo']"
            }
        ]
    }
    saida = executar_scraping(query)
    print(saida)
