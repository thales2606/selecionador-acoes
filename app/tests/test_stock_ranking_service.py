"""Testes para StockRankingService"""

import unittest
import pandas as pd
import numpy as np
from src.domain.services.stock_ranking_service import StockRankingService


class TestStockRankingService(unittest.TestCase):
    """Testes para StockRankingService"""

    def setUp(self):
        """Configura os dados de teste"""
        self.ranking_service = StockRankingService()

    def test_calculate_book_to_market(self):
        """Testa cálculo de Book to Market"""
        df = pd.DataFrame({
            'Ação': ['STOCK1', 'STOCK2'],
            'patrimonio_liquido': ['1.000.000,00', '2.000.000,00'],
            'Market Cap (R$)': ['5.000.000,00', '5.000.000,00'],
            'Financeira': ['Não', 'Não']
        })

        result = self.ranking_service._calculate_book_to_market(df)

        # STOCK1: 1.000.000 / 5.000.000 = 0.2
        # STOCK2: 2.000.000 / 5.000.000 = 0.4
        self.assertAlmostEqual(result.iloc[0], 0.2, places=2)
        self.assertAlmostEqual(result.iloc[1], 0.4, places=2)

    def test_calculate_cash_flow_yield_non_financial(self):
        """Testa cálculo de Cash Flow Yield para ações não-financeiras"""
        df = pd.DataFrame({
            'Ação': ['STOCK1', 'STOCK2'],
            'EV/FCO': [5.0, 10.0],
            'Financeira': ['Não', 'Não']
        })

        result = self.ranking_service._calculate_cash_flow_yield(df)

        # STOCK1: 1 / 5 = 0.2
        # STOCK2: 1 / 10 = 0.1
        self.assertAlmostEqual(result.iloc[0], 0.2, places=2)
        self.assertAlmostEqual(result.iloc[1], 0.1, places=2)

    def test_calculate_cash_flow_yield_financial(self):
        """Testa que Cash Flow Yield retorna NaN para ações financeiras"""
        df = pd.DataFrame({
            'Ação': ['STOCK1', 'STOCK2'],
            'EV/FCO': [5.0, 10.0],
            'Financeira': ['Sim', 'Sim']
        })

        result = self.ranking_service._calculate_cash_flow_yield(df)

        # Deve ser None para financeiras
        self.assertIsNone(result.iloc[0])
        self.assertIsNone(result.iloc[1])

    def test_calculate_earning_yield_non_financial(self):
        """Testa cálculo de Earning Yield para ações não-financeiras"""
        df = pd.DataFrame({
            'Ação': ['STOCK1', 'STOCK2'],
            'EV/EBIT': [5.0, 10.0],
            'Financeira': ['Não', 'Não']
        })

        result = self.ranking_service._calculate_earning_yield(df)

        # STOCK1: 1 / 5 = 0.2
        # STOCK2: 1 / 10 = 0.1
        self.assertAlmostEqual(result.iloc[0], 0.2, places=2)
        self.assertAlmostEqual(result.iloc[1], 0.1, places=2)

    def test_calculate_earning_yield_financial(self):
        """Testa cálculo de Earning Yield para ações financeiras"""
        df = pd.DataFrame({
            'Ação': ['STOCK1', 'STOCK2'],
            'lucro_liquido_anual': ['1.000.000,00', '2.000.000,00'],
            'imposto_anual': ['200.000,00', '400.000,00'],
            'Market Cap (R$)': ['10.000.000,00', '10.000.000,00'],
            'Financeira': ['Sim', 'Sim']
        })

        result = self.ranking_service._calculate_earning_yield(df)

        # STOCK1: (1.000.000 + 200.000) / 10.000.000 = 0.12
        # STOCK2: (2.000.000 + 400.000) / 10.000.000 = 0.24
        self.assertAlmostEqual(result.iloc[0], 0.12, places=2)
        self.assertAlmostEqual(result.iloc[1], 0.24, places=2)

    def test_calculate_ranking_indicators(self):
        """Testa cálculo completo de indicadores de ranking"""
        df = pd.DataFrame({
            'Ação': ['STOCK1', 'STOCK2'],
            'Empresa': ['Company 1', 'Company 2'],
            'patrimonio_liquido': ['1.000.000,00', '2.000.000,00'],
            'Market Cap (R$)': ['5.000.000,00', '5.000.000,00'],
            'EV/FCO': [5.0, 10.0],
            'EV/EBIT': [4.0, 8.0],
            'lucro_liquido_anual': ['1.000.000,00', '2.000.000,00'],
            'imposto_anual': ['200.000,00', '400.000,00'],
            'Financeira': ['Não', 'Não']
        })

        result = self.ranking_service.calculate_ranking_indicators(df)

        # Deve adicionar três colunas
        self.assertIn('Book to Market', result.columns)
        self.assertIn('Cash Flow Yield', result.columns)
        self.assertIn('Earning Yield', result.columns)

        # Deve manter o número de linhas
        self.assertEqual(len(result), 2)

    def test_convert_and_get_float(self):
        """Testa helper de conversão de valores"""
        row = pd.Series({
            'str_value': '1.234.567,89',
            'float_value': 123.45,
            'none_value': None,
            'empty_value': ''
        })

        # Testa string
        result = self.ranking_service._convert_and_get_float(row, 'str_value')
        self.assertAlmostEqual(result, 1234567.89, places=2)

        # Testa float
        result = self.ranking_service._convert_and_get_float(row, 'float_value')
        self.assertAlmostEqual(result, 123.45, places=2)

        # Testa None
        result = self.ranking_service._convert_and_get_float(row, 'none_value')
        self.assertIsNone(result)

        # Testa vazio
        result = self.ranking_service._convert_and_get_float(row, 'empty_value')
        self.assertIsNone(result)

        # Testa coluna inexistente
        result = self.ranking_service._convert_and_get_float(row, 'nonexistent')
        self.assertIsNone(result)

    def test_ranking_with_missing_data(self):
        """Testa comportamento com dados faltantes"""
        df = pd.DataFrame({
            'Ação': ['STOCK1', 'STOCK2', 'STOCK3'],
            'Empresa': ['Company 1', 'Company 2', 'Company 3'],
            'patrimonio_liquido': ['1.000.000,00', None, '3.000.000,00'],
            'Market Cap (R$)': ['5.000.000,00', '5.000.000,00', None],
            'EV/FCO': [5.0, None, 10.0],
            'EV/EBIT': [4.0, 8.0, None],
            'lucro_liquido_anual': ['1.000.000,00', '2.000.000,00', '3.000.000,00'],
            'imposto_anual': ['200.000,00', '400.000,00', '600.000,00'],
            'Financeira': ['Não', 'Não', 'Não']
        })

        result = self.ranking_service.calculate_ranking_indicators(df)

        # Deve continuar com 3 linhas
        self.assertEqual(len(result), 3)

        # STOCK1 deve ter valores calculados
        self.assertIsNotNone(result.iloc[0]['Book to Market'])

        # STOCK2 com patrimonio faltando deve ter NaN ou None
        btm_value = result.iloc[1]['Book to Market']
        self.assertTrue(btm_value is None or pd.isna(btm_value))

        # STOCK3 com Market Cap faltando deve ter NaN ou None
        btm_value = result.iloc[2]['Book to Market']
        self.assertTrue(btm_value is None or pd.isna(btm_value))


if __name__ == '__main__':
    unittest.main()
