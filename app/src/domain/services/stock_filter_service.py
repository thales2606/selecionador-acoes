from typing import List
import pandas as pd
from src.common.value_converters import convert_string_to_float


class StockFilterService:
    """Serviço de domínio para filtros de stocks"""

    def apply_all_filters(self, df: pd.DataFrame) -> pd.DataFrame:
        """Aplica todos os filtros aos dados"""
        df = self._remove_bdrs(df)
        df = self._remove_duplicates_keeping_highest_volume(df)
        df = self._remove_empty_ebit_margin(df)
        df = self._remove_judicial_recovery(df)
        df = self._remove_negative_net_profit(df)
        df = self._remove_top_10_percent_volatility(df)
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

    @staticmethod
    def _remove_judicial_recovery(df: pd.DataFrame) -> pd.DataFrame:
        """Remove empresas em recuperação judicial"""
        initial_count = len(df)
        df = df[~df['situacao_empresa'].str.contains('Recuperação Judicial', case=False, na=False)]
        removed_count = initial_count - len(df)
        if removed_count > 0:
            print(f"Removidas {removed_count} empresas em recuperação judicial")
        return df

    @staticmethod
    def _remove_negative_net_profit(df: pd.DataFrame) -> pd.DataFrame:
        """Remove empresas com lucro líquido negativo (anual ou trimestral)"""
        initial_count = len(df)
        
        # Converte valores de lucro para float
        df['lucro_liquido_anual_float'] = df['lucro_liquido_anual'].apply(convert_string_to_float)
        df['lucro_liquido_trimestral_float'] = df['lucro_liquido_trimestral'].apply(convert_string_to_float)
        
        # Remove se lucro anual OU trimestral é negativo ou None
        mask_negative_annual = df['lucro_liquido_anual_float'].isna() | (df['lucro_liquido_anual_float'] < 0)
        mask_negative_quarterly = df['lucro_liquido_trimestral_float'].isna() | (df['lucro_liquido_trimestral_float'] < 0)
        
        df = df[~(mask_negative_annual | mask_negative_quarterly)]
        
        # Remove as colunas temporárias
        df = df.drop(['lucro_liquido_anual_float', 'lucro_liquido_trimestral_float'], axis=1)
        
        removed_count = initial_count - len(df)
        if removed_count > 0:
            print(f"Removidas {removed_count} empresas com lucro líquido negativo")
        return df

    @staticmethod
    def _remove_top_10_percent_volatility(df: pd.DataFrame) -> pd.DataFrame:
        """Remove as 10% de empresas com maior volatilidade"""
        initial_count = len(df)
        
        if 'Volatilidade Anual (%)' not in df.columns or df['Volatilidade Anual (%)'].isna().all():
            print("Coluna de volatilidade não encontrada ou vazia, pulando filtro")
            return df
        
        # Calcula o 90º percentil
        percentile_90 = df['Volatilidade Anual (%)'].quantile(0.9)
        
        # Remove as empresas acima do 90º percentil
        df = df[df['Volatilidade Anual (%)'] <= percentile_90]
        
        removed_count = initial_count - len(df)
        if removed_count > 0:
            print(f"Removidas {removed_count} empresas com alta volatilidade (> {percentile_90:.2f}%)")
        return df

