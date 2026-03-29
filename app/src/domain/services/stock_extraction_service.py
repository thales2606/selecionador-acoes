import pandas as pd
from typing import List

from six import StringIO

class StockExtractionService:
    """Serviço para extrair dados de stocks do HTML"""

    COLUMN_NAMES = [
        'Ação', 'Empresa', 'Preço', 'Data Preço', 'Data Dem.Financ.', 
        'Consolidação', 'ROInvC', 'Margem Líquida', 'Margem EBIT', 'EV/EBIT', 'EV/FCO', 'Div.Yield',
        'Volume Financ.(R$)', 'Market Cap (R$)'
    ]
    FINANCIAL_COLUMN_NAMES = [
        'Ação', 'Empresa', 'Preço', 'Data Preço', 'Data Dem.Financ.',
        'Consolidação', 'Margem Líquida', 'Div.Yield', 'Market Cap (R$)', 'Volume Financ.(R$)'
    ]
    def extract_from_html(self, html_content: str, financials: bool) -> pd.DataFrame:
        """Extrai dados de stocks do HTML"""
        df_raw = pd.read_html(
            StringIO(html_content),
            header=0,
            decimal=',',
            thousands='.'
        )
        df = df_raw[0]
        df.columns = self.COLUMN_NAMES if not financials else self.FINANCIAL_COLUMN_NAMES
        # Adiciona coluna indicando se é financeira ou não
        df.insert(1, 'Financeira', 'Sim' if financials else 'Não')
        return df
