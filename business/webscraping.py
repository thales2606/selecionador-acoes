from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

class WebScraping:

    def __init__(self, url, chromeDrivePath = '/usr/local/bin/chromedriver'):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        self.drive = webdriver.Chrome(chromeDrivePath, chrome_options=chrome_options)
        if url is not None:
            self.drive.get(url)

    def pegar_conteudo_outerhtml(self, xPath):
        return self.get_element_by_xpath(xPath).get_attribute('outerHTML')
    
    def pegar_conteudo_innerhtml(self, xPath):
        return self.get_element_by_xpath(xPath).get_attribute('innerHTML')

    def get_element_by_xpath(self, xPath):
        return self.drive.find_element(by=By.XPATH, value=xPath)

    def click(self, xPath):
        self.drive.find_element(by=By.XPATH, value=xPath).click()

    def finalizar(self):
        self.drive.quit()
