"""Serviço de domínio para cálculo de indicadores de ranking"""

import pandas as pd
import logging
from src.common.value_converters import convert_string_to_float

logger = logging.getLogger(__name__)


class StockRankingService:
    """Serviço de domínio para calcular indicadores de ranking de ações"""

    def calculate_ranking_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcula indicadores de ranking para cada ação.
        
        Adiciona colunas:
        - Book to Market: Patrimônio Líquido / Market Cap (ambas)
        - Cash Flow Yield: 1 / (EV/FCO) para não-financeiras, NaN para financeiras
        - Earning Yield: EBIT/EV para não-financeiras, (Lucro Antes IR) / Market Cap para financeiras
        
        Args:
            df: DataFrame com dados de ações enriquecidos
            
        Returns:
            DataFrame com colunas de indicadores adicionadas
        """
        print("Calculando indicadores de ranking...")
        
        df = df.copy()
        
        # Calcula Book to Market
        df['Book to Market'] = self._calculate_book_to_market(df)
        
        # Calcula Cash Flow Yield
        df['Cash Flow Yield'] = self._calculate_cash_flow_yield(df)
        
        # Calcula Earning Yield
        df['Earning Yield'] = self._calculate_earning_yield(df)
        
        print("Indicadores de ranking calculados com sucesso!")
        return df

    def _calculate_book_to_market(self, df: pd.DataFrame) -> pd.Series:
        """
        Calcula Book to Market = Patrimônio Líquido / Market Cap
        
        Aplicável para ambas financeiras e não-financeiras.
        Maior é melhor (ação subavaliada).
        """
        btm_values = []
        
        for idx, row in df.iterrows():
            patrimonio = self._convert_and_get_float(row, 'patrimonio_liquido')
            market_cap = self._convert_and_get_float(row, 'Market Cap (R$)')
            
            if patrimonio is not None and market_cap is not None and market_cap != 0:
                btm = patrimonio / market_cap
                btm_values.append(btm)
            else:
                btm_values.append(None)
        
        return pd.Series(btm_values, index=df.index)

    def _calculate_cash_flow_yield(self, df: pd.DataFrame) -> pd.Series:
        """
        Calcula Cash Flow Yield = 1 / (EV/FCO) ou equivalentemente FCO / EV
        
        Aplicável apenas para ações não-financeiras.
        Para financeiras, retorna NaN.
        Maior é melhor.
        """
        cfy_values = []
        
        for idx, row in df.iterrows():
            # Se é financeira, deixa NaN
            if pd.notna(row.get('Financeira')) and row['Financeira'] == 'Sim':
                cfy_values.append(None)
                continue
            
            # Para não-financeiras, tenta usar EV/FCO
            ev_fco = self._convert_and_get_float(row, 'EV/FCO')
            
            if ev_fco is not None and ev_fco != 0:
                cfy = 1 / ev_fco
                cfy_values.append(cfy)
            else:
                cfy_values.append(None)
        
        return pd.Series(cfy_values, index=df.index)

    def _calculate_earning_yield(self, df: pd.DataFrame) -> pd.Series:
        """
        Calcula Earning Yield Operacional.
        
        Para não-financeiras: EBIT / EV = 1 / (EV/EBIT)
        Para financeiras: Lucro Antes do Imposto de Renda / Market Cap
        
        Maior é melhor.
        """
        ey_values = []
        
        for idx, row in df.iterrows():
            # Se é financeira, usa: (Lucro Líquido + Imposto) / Market Cap
            if pd.notna(row.get('Financeira')) and row['Financeira'] == 'Sim':
                lucro_liquido = self._convert_and_get_float(row, 'lucro_liquido_anual')
                imposto = self._convert_and_get_float(row, 'imposto_anual')
                market_cap = self._convert_and_get_float(row, 'Market Cap (R$)')
                
                if (lucro_liquido is not None and imposto is not None and 
                    market_cap is not None and market_cap != 0):
                    ebit = lucro_liquido + imposto
                    ey = ebit / market_cap
                    ey_values.append(ey)
                else:
                    ey_values.append(None)
            else:
                # Para não-financeiras: 1 / (EV/EBIT)
                ev_ebit = self._convert_and_get_float(row, 'EV/EBIT')
                
                if ev_ebit is not None and ev_ebit != 0:
                    ey = 1 / ev_ebit
                    ey_values.append(ey)
                else:
                    ey_values.append(None)
        
        return pd.Series(ey_values, index=df.index)

    @staticmethod
    def _convert_and_get_float(row: pd.Series, column_name: str) -> float | None:
        """
        Helper para converter valor de uma coluna para float.
        
        Tenta primeiro como float nativo, depois como string convertível.
        
        Args:
            row: Serie do pandas representando uma linha
            column_name: Nome da coluna
            
        Returns:
            Valor float ou None se não conseguir converter
        """
        if column_name not in row.index:
            return None
        
        value = row[column_name]
        
        # Se já é float (incluindo NaN)
        if isinstance(value, float):
            return value if pd.notna(value) else None
        
        # Se é string ou outro tipo, tenta converter
        if value is not None:
            return convert_string_to_float(value)
        
        return None
