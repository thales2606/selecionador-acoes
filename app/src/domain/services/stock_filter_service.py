from typing import List
import pandas as pd


class StockFilterService:
    """Serviço de domínio para filtros de stocks"""

    def apply_all_filters(self, df: pd.DataFrame) -> pd.DataFrame:
        """Aplica todos os filtros aos dados"""
        df = self._remove_bdrs(df)
        df = self._remove_duplicates_keeping_highest_volume(df)
        df = self._remove_empty_ebit_margin(df)
        # df = self._sort_by_ev_ebit_asc(df)
        # df = self._rank_by_ev_ebit_asc(df)
        return df

    @staticmethod
    def _remove_bdrs(df: pd.DataFrame) -> pd.DataFrame:
        """Remove BDRs (contêm '33' no ticker)"""
        df = df[~df['Ação'].str.contains('33')]
        return df

    @staticmethod
    def _remove_duplicates_keeping_highest_volume(df: pd.DataFrame) -> pd.DataFrame:
        """Remove duplicatas, mantendo apenas a com maior volume financeiro"""
        df = df.sort_values("Volume Financ.(R$)")
        df = df.drop_duplicates(subset='Empresa', keep='last')
        return df

    @staticmethod
    def _remove_empty_ebit_margin(df: pd.DataFrame) -> pd.DataFrame:
        """Remove linhas com margem EBIT vazia apenas para ações não-financeiras"""
        # Remove linhas com margem EBIT vazia apenas se É Financeira == 'Não'
        mask_non_financial = df['Financeira'] == 'Não'
        mask_empty_ebit = df['Margem EBIT'].isna()
        df = df[~(mask_non_financial & mask_empty_ebit)]
        return df

    @staticmethod
    def _sort_by_ev_ebit_asc(df: pd.DataFrame) -> pd.DataFrame:
        """Ordena por EV/EBIT em ordem ascendente"""
        df = df.sort_values("EV/EBIT")
        return df

    @staticmethod
    def _rank_by_ev_ebit_asc(df: pd.DataFrame) -> pd.DataFrame:
        """Classifica por EV/EBIT"""
        df['Rank EV/EBIT'] = df[['EV/EBIT', 'Ação']].apply(tuple, axis=1)\
            .rank(method='dense', ascending=True).astype(int)
        return df
