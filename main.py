import pandas
from business.filter_stock_scraping import FiltroAcoesScraping
from business.filtros import Filtros
from business.principais_indicadores_scraping import PrincipaisIndicadoresScraping
from business.selecao_acoes_scraping import SelecaoAcoesScraping
from business.webscraping import WebScraping
import time
import json

url = "https://www.fundamentus.com.br/buscaavancada.php"
web_scraping = WebScraping(url)
filtro_acoes_scraping = FiltroAcoesScraping(web_scraping)
selecao_acoes_scraping = SelecaoAcoesScraping(web_scraping)
principais_indicadores_scraping = PrincipaisIndicadoresScraping(web_scraping)

try:
    settings = json.load(open('settings.json'))
    filter_types = ["valor-da-empresa-sobre-ebit", "margem-ebit"]
    filters = []    
    for filter in settings['filters']:
        if filter['name'] in filter_types:
            filter['minValue'] = '0'
            filter['maxValue'] = ''
            filters.append(filter)   
    
    filtro_acoes_scraping.filter(filters)
    time.sleep(2)
    html_content = selecao_acoes_scraping.pegar_tabela_resultante()

    df_full = pandas.read_html(
        str(html_content), header=0, decimal=',', thousands='.')
    df = df_full[0]

    df.columns = ['Papel', 'Cotação', 'P/L', 'P/VP', 'PSR', 'Div.Yield', 'P/Ativo', 
                  'P/Cap.Giro', 'P/EBIT', 'P/Ativ Circ.Liq', 'EV/EBIT', 'EV/EBITDA', 
                  'Mrg Ebit', 'Mrg. Líq.', 'Liq. Corr.', 'ROIC', 'ROE', 'Liq.2meses', 
                  'Patrim. Líq', 'Dív.Brut/ Patrim.', 'Cresc. Rec.5a']
    df = Filtros().aplicar_filtros(df)
        
    df.to_excel(excel_writer='C:\\Users\\thale\\OneDrive\\Área de Trabalho\\Rancking_acoes_brasileiras.xlsx',
                sheet_name='Rancking de açoes Brasileiras')

finally:
    web_scraping.finalizar()
