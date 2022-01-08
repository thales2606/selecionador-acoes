import pandas
from business.filtro_acoes_scraping import FiltroAcoesScraping
from business.filtros import Filtros
from business.principais_indicadores_scraping import PrincipaisIndicadoresScraping
from business.selecao_acoes_scraping import SelecaoAcoesScraping
from business.webscraping import WebScraping
import time

url = "https://www.investsite.com.br/seleciona_acoes.php"
web_scraping = WebScraping(url)
filtro_acoes_scraping = FiltroAcoesScraping(web_scraping)
selecao_acoes_scraping = SelecaoAcoesScraping(web_scraping)
principais_indicadores_scraping = PrincipaisIndicadoresScraping(web_scraping)

try:
    filtro_acoes_scraping.realizar_filtro()
    html_content = selecao_acoes_scraping.pegar_tabela_resultante()

    df_full = pandas.read_html(
        str(html_content), header=0, decimal=',', thousands='.')
    df = df_full[0]
    df.columns = ['Ação', 'Empresa', 'Preço', 'ROInvC',
                  'Margem EBIT', 'EV/EBIT', 'DY', 'Volume Financ.(R$)', 'Market Cap (R$)']
    df = Filtros().aplicar_filtros(df)

    for index, row in df.iterrows():
        principais_indicadores_scraping.proximo(row['Ação'])
        time.sleep(1)
        divida_liquida = principais_indicadores_scraping.buscar_divida_liquida()
        ebit = principais_indicadores_scraping.buscar_ebit()
        quantidade_total_acoes = principais_indicadores_scraping.buscar_quantidade_total_acoes()
        df.loc[index, 'Earning Yield'] = ebit / \
            ((quantidade_total_acoes + divida_liquida) * row['Preço'])

    df.to_excel(excel_writer='C:\\Users\\HOME\\OneDrive\\Finanças\\Rancking_acoes_brasileiras.xlsx',
                sheet_name='Rancking de açoes Brasileiras')

finally:
    web_scraping.finalizar()
