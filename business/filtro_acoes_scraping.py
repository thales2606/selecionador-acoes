from selenium.webdriver.support.ui import Select


class FiltroAcoesScraping:
    checkSelectAll = '//*[@id="selectAll"]'
    checkMargemEBIT = '//*[@id="coluna10"]'
    checkEVEBIT = '//*[@id="coluna23"]'
    checkVolumeFinanceiro = '//*[@id="coluna26"]'
    checkMarketCap = '//*[@id="coluna27"]'
    inputVolumeFinanceiroMinimo = '//*[@id="tabela_seleciona_acoes"]/tbody/tr[24]/td[2]/input'
    inputMargemEBIT = '//*[@id="tabela_seleciona_acoes"]/tbody/tr[8]/td[2]/input'
    buttonProcurarAcoes = '//*[@id="form_seleciona_acoes"]/input[1]'
    volumeFinanceiroMinimo = '200000'
    MargemEBITMinimo = '0'
    select_numero_resultados = '//*[@id="num_result"]'

    def __init__(self, web_scraping):
        self.web_Scraping = web_scraping

    def realizar_filtro(self):
        self.selecionar_todos_checks()
        self.selecionar_todos_checks()
        select = Select(self.web_Scraping.get_element_by_xpath(
            self.select_numero_resultados))
        select.select_by_value('todos')
        self.web_Scraping.click(self.checkMargemEBIT)
        self.web_Scraping.click(self.checkEVEBIT)
        self.web_Scraping.click(self.checkVolumeFinanceiro)
        self.web_Scraping.click(self.checkMarketCap)
        self.inserir_valor_em_campo(
            self.inputVolumeFinanceiroMinimo, self.volumeFinanceiroMinimo)
        self.inserir_valor_em_campo(
            self.inputMargemEBIT, self.MargemEBITMinimo)
        self.web_Scraping.get_element_by_xpath(self.buttonProcurarAcoes).click()

    def selecionar_todos_checks(self):
        self.web_Scraping.click(self.checkSelectAll)

    def inserir_valor_em_campo(self, xPath, valor):
        self.web_Scraping.get_element_by_xpath(xPath
                                              ).send_keys(valor)
