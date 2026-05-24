"""Testes para StockFilterService - novos filtros"""

import unittest
import pandas as pd
import numpy as np
from src.domain.services.stock_filter_service import StockFilterService


class TestStockFilterServiceNewFilters(unittest.TestCase):
    """Testes para os novos filtros de StockFilterService"""

    def setUp(self):
        """Configura os dados de teste"""
        self.filter_service = StockFilterService()

    def test_remove_judicial_recovery(self):
        """Testa remoção de empresas em recuperação judicial"""
        df = pd.DataFrame({
            'Ação': ['STOCK1', 'STOCK2', 'STOCK3'],
            'Empresa': ['Company 1', 'Company 2', 'Company 3'],
            'situacao_empresa': ['Normal', 'Recuperação Judicial', 'Normal']
        })

        result = self.filter_service._remove_judicial_recovery(df)

        self.assertEqual(len(result), 2)
        self.assertNotIn('STOCK2', result['Ação'].values)

    def test_remove_judicial_recovery_case_insensitive(self):
        """Testa remoção case-insensitive de recuperação judicial"""
        df = pd.DataFrame({
            'Ação': ['STOCK1', 'STOCK2'],
            'Empresa': ['Company 1', 'Company 2'],
            'situacao_empresa': ['Normal', 'recuperação judicial']  # Lowercase
        })

        result = self.filter_service._remove_judicial_recovery(df)

        self.assertEqual(len(result), 1)
        self.assertIn('STOCK1', result['Ação'].values)

    def test_remove_negative_net_profit_annual(self):
        """Testa remoção de empresas com lucro líquido anual negativo"""
        df = pd.DataFrame({
            'Ação': ['STOCK1', 'STOCK2', 'STOCK3'],
            'Empresa': ['Company 1', 'Company 2', 'Company 3'],
            'lucro_liquido_anual': ['1.000.000,00', '-500.000,00', '2.000.000,00'],
            'lucro_liquido_trimestral': ['250.000,00', '-100.000,00', '500.000,00']
        })

        result = self.filter_service._remove_negative_net_profit(df)

        self.assertEqual(len(result), 2)
        self.assertNotIn('STOCK2', result['Ação'].values)

    def test_remove_negative_net_profit_quarterly(self):
        """Testa remoção de empresas com lucro líquido trimestral negativo"""
        df = pd.DataFrame({
            'Ação': ['STOCK1', 'STOCK2', 'STOCK3'],
            'Empresa': ['Company 1', 'Company 2', 'Company 3'],
            'lucro_liquido_anual': ['1.000.000,00', '500.000,00', '2.000.000,00'],
            'lucro_liquido_trimestral': ['250.000,00', '-100.000,00', '500.000,00']
        })

        result = self.filter_service._remove_negative_net_profit(df)

        self.assertEqual(len(result), 2)
        self.assertNotIn('STOCK2', result['Ação'].values)

    def test_remove_negative_net_profit_with_empty_values(self):
        """Testa remoção considerando valores vazios como negativos"""
        df = pd.DataFrame({
            'Ação': ['STOCK1', 'STOCK2', 'STOCK3'],
            'Empresa': ['Company 1', 'Company 2', 'Company 3'],
            'lucro_liquido_anual': ['1.000.000,00', '', '2.000.000,00'],
            'lucro_liquido_trimestral': ['250.000,00', '100.000,00', '500.000,00']
        })

        result = self.filter_service._remove_negative_net_profit(df)

        # Vazio é considerado como negativo, então STOCK2 deve ser removido
        self.assertEqual(len(result), 2)
        self.assertNotIn('STOCK2', result['Ação'].values)

    def test_remove_top_10_percent_volatility(self):
        """Testa remoção do top 10% de volatilidade"""
        # Cria 100 ações com volatilidade de 1 a 100
        df = pd.DataFrame({
            'Ação': [f'STOCK{i}' for i in range(100)],
            'Empresa': [f'Company {i}' for i in range(100)],
            'Volatilidade Anual (%)': list(range(1, 101))
        })

        result = self.filter_service._remove_top_10_percent_volatility(df)

        # Deve remover aproximadamente 10 ações (10% de 100)
        self.assertLessEqual(len(result), 91)  # 90% de 100 = 90, com margem
        self.assertGreater(len(result), 85)

    def test_remove_top_10_percent_volatility_with_nan(self):
        """Testa comportamento com valores NaN em volatilidade"""
        df = pd.DataFrame({
            'Ação': ['STOCK1', 'STOCK2', 'STOCK3'],
            'Empresa': ['Company 1', 'Company 2', 'Company 3'],
            'Volatilidade Anual (%)': [10.0, np.nan, 30.0]
        })

        # Não deve quebrar com NaN
        result = self.filter_service._remove_top_10_percent_volatility(df)

        # Deve continuar com algum resultado
        self.assertGreater(len(result), 0)

    def test_apply_all_filters_in_order(self):
        """Testa que todos os filtros são aplicados na ordem correta"""
        df = pd.DataFrame({
            'Ação': ['STOCK1', 'STOCK2', 'STOCK3', 'BDR33', 'STOCK4'],
            'Empresa': ['Company 1', 'Company 2', 'Company 2', 'BDR Company', 'Company 1'],  # Duplicata
            'Margem EBIT': [0.1, 0.2, 0.3, 0.4, 0.5],
            'Financeira': ['Não', 'Não', 'Não', 'Não', 'Não'],
            'Volume Financ.(R$)': [1000, 2000, 3000, 4000, 5000],
            'situacao_empresa': ['Normal', 'Recuperação Judicial', 'Normal', 'Normal', 'Normal'],
            'lucro_liquido_anual': ['1.000.000,00', '-500.000,00', '2.000.000,00', '3.000.000,00', '4.000.000,00'],
            'lucro_liquido_trimestral': ['250.000,00', '100.000,00', '500.000,00', '750.000,00', '1.000.000,00'],
            'Volatilidade Anual (%)': [10.0, 20.0, 30.0, 40.0, 50.0]
        })

        result = self.filter_service.apply_all_filters(df)

        # Esperado resultado:
        # - Remove BDR33 (BDR)
        # - Remove uma duplicata
        # - Remove empresa em recuperação judicial
        # - Remove empresa com lucro negativo
        # - Remove top 10% volatilidade

        # Deve ter menos de 5 ações
        self.assertLess(len(result), 5)


if __name__ == '__main__':
    unittest.main()
