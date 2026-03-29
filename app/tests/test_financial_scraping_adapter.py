"""
Testes unitários para o adapter de ações financeiras
"""

import unittest
from unittest.mock import Mock, MagicMock, patch

from src.rank.adapters.outbound.scraping.invest_site_financial_scraping_adapter import (
    InvestSiteFinancialScrapingAdapter
)


class TestInvestSiteFinancialScrapingAdapter(unittest.TestCase):
    """Testes para o adapter de scraping de ações financeiras"""

    def setUp(self):
        """Configura os mocks antes de cada teste"""
        self.mock_web_scraping = Mock()
        self.adapter = InvestSiteFinancialScrapingAdapter(self.mock_web_scraping)

    def test_adapter_initialization(self):
        """Testa se o adapter é inicializado corretamente"""
        self.assertIsNotNone(self.adapter)
        self.assertEqual(self.adapter.web_scraping, self.mock_web_scraping)

    def test_apply_filters_calls_select_filter(self):
        """Testa se apply_filters chama _select_filter para cada filtro"""
        with patch.object(self.adapter, '_select_filter') as mock_select:
            self.adapter.apply_filters()
            # Verifica se _select_filter foi chamado 8 vezes (um para cada filtro)
            self.assertEqual(mock_select.call_count, 8)

    def test_apply_filters_sends_volume_minimum(self):
        """Testa se o volume mínimo é enviado corretamente"""
        with patch.object(self.adapter, '_select_filter'):
            self.adapter.apply_filters()
            self.mock_web_scraping.send_keys_to_element.assert_called_once_with(
                self.adapter.INPUT_VOLUME_MINIMO,
                self.adapter.VOLUME_MINIMO
            )

    def test_apply_filters_clicks_search_button(self):
        """Testa se o botão de busca é clicado"""
        with patch.object(self.adapter, '_select_filter'):
            self.adapter.apply_filters()
            self.mock_web_scraping.click_element.assert_called_with(
                self.adapter.BUTTON_PROCURAR
            )

    def test_get_results_table_returns_html(self):
        """Testa se get_results_table retorna o HTML"""
        expected_html = "<table>...</table>"
        self.mock_web_scraping.get_element_html.return_value = expected_html

        result = self.adapter.get_results_table()

        self.assertEqual(result, expected_html)
        self.mock_web_scraping.get_element_html.assert_called_with(
            self.adapter.TABELA_RESULTADOS
        )

    def test_get_results_table_handles_dropdown_error(self):
        """Testa se get_results_table continua mesmo se dropdown falhar"""
        self.mock_web_scraping.select_dropdown_value.side_effect = Exception("Erro")
        self.mock_web_scraping.get_element_html.return_value = "<table>...</table>"

        # Não deve lançar exceção
        result = self.adapter.get_results_table()

        self.assertIsNotNone(result)

    def test_select_filter_scrolls_to_element(self):
        """Testa se _select_filter faz scroll até o elemento"""
        xpath = '//*[@id="itm7"]'

        with patch('time.sleep'):
            self.adapter._select_filter(xpath)

        self.mock_web_scraping.scroll_to_element.assert_called_with(xpath)

    def test_select_filter_clicks_element(self):
        """Testa se _select_filter clica no elemento"""
        xpath = '//*[@id="itm7"]'

        with patch('time.sleep'):
            self.adapter._select_filter(xpath)

        self.mock_web_scraping.click_element.assert_called_with(xpath)

    def test_volume_minimo_constant(self):
        """Testa se a constante de volume mínimo está correta"""
        self.assertEqual(self.adapter.VOLUME_MINIMO, '3000000')

    def test_xpaths_for_financial_filters(self):
        """Testa se os XPaths dos filtros estão definidos"""
        self.assertIsNotNone(self.adapter.CHECK_ROE)
        self.assertIsNotNone(self.adapter.CHECK_MARGEM_LIQUIDA)
        self.assertIsNotNone(self.adapter.CHECK_ALAVANCAGEM)
        self.assertIsNotNone(self.adapter.CHECK_PE)
        self.assertIsNotNone(self.adapter.CHECK_PB)
        self.assertIsNotNone(self.adapter.CHECK_DY)
        self.assertIsNotNone(self.adapter.CHECK_VOLUME_FINANCEIRO)
        self.assertIsNotNone(self.adapter.CHECK_MARKET_CAP)


if __name__ == '__main__':
    unittest.main()

