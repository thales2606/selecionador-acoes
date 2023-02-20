import unittest
from unittest.mock import patch
from http.client import BAD_REQUEST, OK
import json
import pandas
from business.filter_stock_scraping import FilterStockScraping
from business.selecao_acoes_scraping import SelecaoAcoesScraping
from business.webscraping import WebScraping
from lambda_function import lambda_handler
import time

class TestLambdaHandler(unittest.TestCase):
    @patch('business.webscraping.WebScraping.finalizar')
    @patch('business.selecao_acoes_scraping.SelecaoAcoesScraping.pegar_tabela_resultante')
    @patch('business.filter_stock_scraping.FilterStockScraping.filter')
    @patch('json.load')
    def test_lambda_handler_success(self, mock_json_load, mock_filter, mock_pegar_tabela_resultante, mock_finalizar):
        mock_json_load.return_value = {
            'filters': [
                {'name': 'preco-por-lucro'},
                {'name': 'preco-por-valor-patrimonial'}
            ]
        }
        mock_filter.return_value = None
        mock_pegar_tabela_resultante.return_value = '<html>...</html>'
        mock_finalizar.return_value = None

        event = {
            'filters': [
                {'name': 'preco-por-lucro'},
                {'name': 'preco-por-valor-patrimonial'}
            ]
        }
        context = None
        result = lambda_handler(event, context)
        self.assertEqual(result['statusCode'], 400)
        self.assertIsNotNone(result['body'])
        mock_json_load.assert_called_once()
        mock_filter.assert_called_once()
        mock_pegar_tabela_resultante.assert_called_once()
        mock_finalizar.assert_called_once()

    @patch('business.webscraping.WebScraping.finalizar')
    @patch('json.load')
    def test_lambda_handler_value_error(self, mock_json_load, mock_finalizar):
        mock_json_load.side_effect = ValueError('Error')
        mock_finalizar.return_value = None

        event = {
            'filters': [
                {'name': 'preco-por-lucro'},
                {'name': 'preco-por-valor-patrimonial'}
            ]
        }
        context = None
        result = lambda_handler(event, context)
        self.assertEqual(result['statusCode'], 400)
        self.assertIsNotNone(result['body'])
        mock_json_load.assert_called_once()
        mock_finalizar.assert_called_once()

if __name__ == '__main__':
    unittest.main()