from selenium.webdriver.support.ui import Select


class FilterStockScraping:
    buttonFindStoks = '/html/body/div[1]/div[2]/form/input'   
    def __init__(self, web_scraping):
        self.web_Scraping = web_scraping

    def filter(self, filters): 
        filter_types = {
            "select" : self.exec_select_command,
            "min-max" : self.exec_min_max_command
        }
        for filter in filters:            
            filter_types[filter['type']](filter)
        self.web_Scraping.get_element_by_xpath(self.buttonFindStoks).click()


    def inserir_valor_em_campo(self, xPath, valor):
        self.web_Scraping.get_element_by_xpath(xPath
                                              ).send_keys(valor)
    
    def exec_min_max_command(self, command):
        self.inserir_valor_em_campo(
                command['minInputTextAddress'], command['minValue'])
        self.inserir_valor_em_campo(
                command['maxInputTextAddress'], command['maxValue'])
    
    def exec_select_command(self, command):
        element = self.web_Scraping.get_element_by_xpath(command['selectComboBoxAddress'])
        select = Select(element)
        select.select_by_value(command['value'])
