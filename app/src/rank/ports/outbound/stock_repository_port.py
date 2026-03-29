from abc import ABC, abstractmethod

import pandas as pd


class StockRepositoryPort(ABC):
    """Interface para repositório de stocks"""

    @abstractmethod
    def save_dataframe(self, df: pd.DataFrame, file_path: str, sheet_name: str) -> None:
        """Salva um DataFrame em um arquivo"""
        pass
