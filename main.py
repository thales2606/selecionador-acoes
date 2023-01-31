import pandas
from business.filter_stock_scraping import FilterStockScraping
from business.selecao_acoes_scraping import SelecaoAcoesScraping
from business.webscraping import WebScraping
import time
import json

url = "https://www.fundamentus.com.br/buscaavancada.php"
web_scraping = WebScraping(url)
filtro_acoes_scraping = FilterStockScraping(web_scraping)
selecao_acoes_scraping = SelecaoAcoesScraping(web_scraping)

event = {
    'filters': [
        {
            "name": "valor-da-empresa-sobre-ebit",
            "type": "min-max",
            "minValue": '0',
            "maxValue": ''
        }
    ]
}

try:
    settings = json.load(open('settings.json'))
    for filter in event['filters']:
        filterSettings = next(x for x in settings['filters'] if x['name'] == filter['name'])
        filter['type'] = filterSettings['type']
        if filterSettings['type'] == 'min-max':
            filter['minInputTextAddress'] = filterSettings['minInputTextAddress']
            filter['maxInputTextAddress'] = filterSettings['maxInputTextAddress']
        if filterSettings['type'] == 'select':
            filter['selectComboBoxAddress'] = filterSettings['selectComboBoxAddress']

    filtro_acoes_scraping.filter(event['filters'])
    html_content = selecao_acoes_scraping.pegar_tabela_resultante()

    df_full = pandas.read_html(
        str(html_content), header=0, decimal=',', thousands='.')
    df = df_full[0]

    df.columns = ['papel', 'cotacao', 'preco-por-lucro', 'preco-por-valor-patrimonial', 'psr', 'dividend-yield', 'preco-por-ativo', 
                'preco-capital-de-giro', 'preco-por-ebit', 'preco-por-ativos-circ-liquido', 'ev-por-ebit', 'ev-por-ebitda', 
                'margem-ebit', 'margem-liquida', 'liquida-corr.', 'roic', 'roe', 'liquida-dois-meses', 
                'patrimonio-liquido', 'divida-bruta-por-patrimonio', 'cresc-rec-cinco-a']

    json_result = df.to_json(orient = 'records')
    print(json_result)
finally:
    web_scraping.finalizar()