from http.client import BAD_REQUEST, OK
import json
import pandas
from business.filter_stock_scraping import FilterStockScraping
from business.selecao_acoes_scraping import SelecaoAcoesScraping
from business.webscraping import WebScraping
import time

def lambda_handler(event, context):
    url = "https://www.fundamentus.com.br/buscaavancada.php"
    web_scraping = WebScraping(url)
    filtro_acoes_scraping = FilterStockScraping(web_scraping)
    selecao_acoes_scraping = SelecaoAcoesScraping(web_scraping)

    try:
        settings = json.load(open('settings.json')) 
        
        filtro_acoes_scraping.filter(event.filters)
        time.sleep(2)
        html_content = selecao_acoes_scraping.pegar_tabela_resultante()

        df_full = pandas.read_html(
            str(html_content), header=0, decimal=',', thousands='.')
        df = df_full[0]

        df.columns = ['Papel', 'Cotação', 'P/L', 'P/VP', 'PSR', 'Div.Yield', 'P/Ativo', 
                    'P/Cap.Giro', 'P/EBIT', 'P/Ativ Circ.Liq', 'EV/EBIT', 'EV/EBITDA', 
                    'Mrg Ebit', 'Mrg. Líq.', 'Liq. Corr.', 'ROIC', 'ROE', 'Liq.2meses', 
                    'Patrim. Líq', 'Dív.Brut/ Patrim.', 'Cresc. Rec.5a']

        json_result = df.to_json(orient = 'columns')
        return json.load(json_result)
    finally:
        web_scraping.finalizar()
        return BAD_REQUEST