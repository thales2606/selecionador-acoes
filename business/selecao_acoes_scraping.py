from selenium.webdriver.support.ui import Select


class SelecaoAcoesScraping:

    select_quantidade_acoes_por_pagina = '//*[@id="tabela_selecao_acoes_length"]/select'
    quantidade_acoes_por_pagina = '1000'
    tabela_selecao_acoes = '//*[@id="resultado"]'

    def __init__(self, web_scraping):
        self.web_Scraping = web_scraping

    def pegar_tabela_resultante(self):       
        html_element = self.web_Scraping.pegar_conteudo_outerhtml(
            self.tabela_selecao_acoes)
        return html_element
