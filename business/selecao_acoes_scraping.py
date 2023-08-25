from selenium.webdriver.support.ui import Select

class SelecaoAcoesScraping:

    select_quantidade_acoes_por_pagina = '//*[@id="tabela_selecao_acoes_length"]/label/select'
    quantidade_acoes_por_pagina = '-1'
    tabela_selecao_acoes = '//*[@id="tabela_selecao_acoes"]'

    def __init__(self, web_scraping):
        self.web_Scraping = web_scraping

    def pegar_tabela_resultante(self):
        select = Select(self.web_Scraping.get_element_by_xpath(
            self.select_quantidade_acoes_por_pagina))
        select.select_by_value(self.quantidade_acoes_por_pagina)
        html_element = self.web_Scraping.pegar_conteudo_outerhtml(
            self.tabela_selecao_acoes)
        return html_element
