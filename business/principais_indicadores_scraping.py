import re
from typing import DefaultDict
from business.webscraping import WebScraping


class PrincipaisIndicadoresScraping:

    label_situacao_emissor = '//*[@id="tabela_resumo_empresa"]/tbody/tr[4]/td[2]'
    label_receita_liquida_ano = '//*[@id="tabela_resumo_empresa_dre_12meses"]/tbody/tr[1]/td[2]'
    label_ebit_ano = '//*[@id="tabela_resumo_empresa_dre_12meses"]/tbody/tr[3]/td[2]'
    url = 'https://www.investsite.com.br/principais_indicadores.php?cod_negociacao='

    def __init__(self):
        self.web_scraping = WebScraping(None)

    def proximo(self, acao):
        self.web_scraping.drive.get(self.url + acao)

    def buscar_situacao_emissor(self):
        return self.web_scraping.pegar_conteudo_innerhtml(self.label_situacao_emissor)

    def buscar_diferenca_ebit_receita_liquida(self):
        receita_liquida = self.retirar_valor_monetario(
            self.web_scraping.pegar_conteudo_innerhtml(self.label_receita_liquida_ano))
        ebit = self.retirar_valor_monetario(
            self.web_scraping.pegar_conteudo_innerhtml(self.label_ebit_ano))
        return ebit - receita_liquida

    def retirar_valor_monetario(self, conteudo):
        resultado = re.sub(r'[^0-9,]', '', str(conteudo))
        expoente = self.pegar_expoente(conteudo[-1])
        return float(resultado.replace(',', '.')) * (10 ** expoente)

    def pegar_expoente(self, conteudo):
        return DefaultDict(lambda: 0, {'m': 6, '9': 9, })[conteudo]

    def finalizar(self):
        self.web_scraping.finalizar()
