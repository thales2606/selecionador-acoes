import time
from selenium.webdriver.support.ui import Select

from business.webscraping import WebScraping


class FiltroAcoesScraping:
    checkSelectAll = '//*[@id="selectAll"]'
    checkROI = '//*[@id="itm8"]'
    checkMargemEBIT = '//*[@id="itm13"]'
    checkEVEBIT = '//*[@id="itm26"]'
    checkDY = '//*[@id="itm32"]'
    checkVolumeFinanceiro = '//*[@id="itm33"]'
    checkMarketCap = '//*[@id="itm34"]'
    inputVolumeFinanceiroMinimo = '//*[@id="tabela_seleciona_acoes"]/tbody/tr[28]/td[2]/input'
    inputMargemEBIT = '//*[@id="tabela_seleciona_acoes"]/tbody/tr[8]/td[2]/input'
    buttonProcurarAcoes = '//*[@id="form_seleciona_acoes"]/div[1]/div[1]/div/div[1]/button'
    volumeFinanceiroMinimo = '3000000'
    MargemEBITMinimo = '0'

    def __init__(self, web_scraping: WebScraping):
        self.web_Scraping = web_scraping

    def realizar_filtro(self):
        self.selecionar_todos_checks()
        self.selecionar_todos_checks()        
                
        self.web_Scraping.scroll_to_element(self.checkROI)
        time.sleep(1)
        self.web_Scraping.click(self.checkROI)

        self.web_Scraping.scroll_to_element(self.checkMargemEBIT)
        time.sleep(1)
        self.web_Scraping.click(self.checkMargemEBIT)

        self.web_Scraping.scroll_to_element(self.checkEVEBIT)
        time.sleep(1)
        self.web_Scraping.click(self.checkEVEBIT)        

        self.web_Scraping.scroll_to_element(self.checkDY)
        time.sleep(1)
        self.web_Scraping.click(self.checkDY)       

        self.web_Scraping.scroll_to_element(self.checkVolumeFinanceiro)
        time.sleep(1)
        self.web_Scraping.click(self.checkVolumeFinanceiro)        

        self.web_Scraping.scroll_to_element(self.checkMarketCap)
        time.sleep(1)
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