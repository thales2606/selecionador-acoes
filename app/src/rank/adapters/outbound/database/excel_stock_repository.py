import pandas as pd
from src.rank.ports.outbound.stock_repository_port import StockRepositoryPort


class ExcelStockRepository(StockRepositoryPort):
    """Adapter para persistência de stocks em Excel"""

    def save_dataframe(self, df: pd.DataFrame, file_path: str, sheet_name: str) -> None:
        """Salva um DataFrame em um arquivo Excel, preservando todas as colunas"""
        # Se o DataFrame tem coluna de volatilidade em formato decimal, converte para percentual
        if 'Volatilidade Anual (%)' in df.columns:
            # A volatilidade já deve estar em formato percentual do método _enrich_with_volatility
            pass

        df.to_excel(
            excel_writer=file_path,
            sheet_name=sheet_name,
            index=False
        )
