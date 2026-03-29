from dependency_injection import initialize_di
from src.rank.adapters.outbound.scraping.web_scraping_driver import WebScrapingDriver


def cleanup(ws: WebScrapingDriver) -> None:
    """Libera recursos"""
    if ws:
        ws.close()

if __name__ == '__main__':
    controller, web_scraping = initialize_di()
    try:
        controller.start_scraping()
    finally:
        cleanup(web_scraping)

    # import yfinance as yf
    # import numpy as np
    #
    # ticker = yf.Ticker("AMER3.SA")
    #
    # # Anual
    # fin_anual = ticker.financials
    # lucro_ultimo_ano = fin_anual.loc["Net Income"].iloc[0]
    # print("Lucro líquido último ano:", lucro_ultimo_ano)
    # # Trimestral
    # q_fin = ticker.quarterly_financials
    # lucro_ultimo_trimestre = q_fin.loc["Net Income"].iloc[0]
    # print("Lucro último trimestre:", lucro_ultimo_trimestre)