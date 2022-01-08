import re
from typing import DefaultDict
from business.webscraping import WebScraping


class PrincipaisIndicadoresScraping:

    label_situacao_emissor = '//*[@id="tabela_resumo_empresa"]/tbody/tr[4]/td[2]'
    label_receita_liquida_ano = '//*[@id="tabela_resumo_empresa_dre_12meses"]/tbody/tr[1]/td[2]'
    label_ebit_ano = '//*[@id="tabela_resumo_empresa_dre_12meses"]/tbody/tr[3]/td[2]'
    label_divida_liquida_conteudo = '//*[@id="tabela_resumo_empresa_bp"]/tbody/tr[6]/td[2]'
    label_quantidade_total_acoes = '//*[@id="tabela_resumo_empresa_bp"]/tbody/tr[10]/td[2]'
    url = 'https://www.investsite.com.br/principais_indicadores.php?cod_negociacao='

    def __init__(self, web_scraping):
        self.web_scraping = web_scraping

    def proximo(self, acao):
        self.web_scraping.drive.get(self.url + acao)

    def buscar_situacao_emissor(self):
        return self.web_scraping.pegar_conteudo_innerhtml(self.label_situacao_emissor)

    def buscar_ebit(self):
        return self.retirar_valor_monetario(
            self.web_scraping.pegar_conteudo_innerhtml(self.label_ebit_ano))

    def buscar_divida_liquida(self):
        return self.retirar_valor_monetario(self.web_scraping.pegar_conteudo_innerhtml(self.label_divida_liquida_conteudo))

    def buscar_quantidade_total_acoes(self):
        quantidade = self.web_scraping.pegar_conteudo_innerhtml(
            self.label_quantidade_total_acoes)
        return self.retirar_valor_monetario(quantidade)

    def retirar_valor_monetario(self, conteudo):
        resultado = re.sub(r'[^0-9,]', '', str(conteudo))
        expoente = self.pegar_expoente(conteudo[-1])
        return float(resultado.replace(',', '.')) * (10 ** expoente)

    def pegar_expoente(self, conteudo):
        return DefaultDict(lambda: 0, {'M': 6, 'B': 9, })[conteudo]
    
