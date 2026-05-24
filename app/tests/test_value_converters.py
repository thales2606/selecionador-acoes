"""Testes para value_converters"""

import unittest
from src.common.value_converters import convert_string_to_float


class TestConvertStringToFloat(unittest.TestCase):
    """Testes para a função de conversão de string para float"""

    def test_convert_float_direct(self):
        """Testa conversão direta de float"""
        result = convert_string_to_float(123.45)
        self.assertEqual(result, 123.45)

    def test_convert_string_with_dot_separator(self):
        """Testa conversão de string com separador de milhares (ponto)"""
        result = convert_string_to_float("1.234.567,89")
        self.assertAlmostEqual(result, 1234567.89, places=2)

    def test_convert_string_without_dot_separator(self):
        """Testa conversão de string sem separador de milhares"""
        result = convert_string_to_float("1234567,89")
        self.assertAlmostEqual(result, 1234567.89, places=2)

    def test_convert_negative_value(self):
        """Testa conversão de valor negativo"""
        result = convert_string_to_float("-123,45")
        self.assertAlmostEqual(result, -123.45, places=2)

    def test_convert_negative_large_value(self):
        """Testa conversão de valor negativo grande"""
        result = convert_string_to_float("-1.234.567,89")
        self.assertAlmostEqual(result, -1234567.89, places=2)

    def test_convert_empty_string(self):
        """Testa conversão de string vazia"""
        result = convert_string_to_float("")
        self.assertIsNone(result)

    def test_convert_whitespace_string(self):
        """Testa conversão de string com apenas espaços"""
        result = convert_string_to_float("   ")
        self.assertIsNone(result)

    def test_convert_none(self):
        """Testa conversão de None"""
        result = convert_string_to_float(None)
        self.assertIsNone(result)

    def test_convert_integer_string(self):
        """Testa conversão de string contendo apenas inteiro"""
        result = convert_string_to_float("1000")
        self.assertEqual(result, 1000.0)

    def test_convert_zero(self):
        """Testa conversão de zero"""
        result = convert_string_to_float("0,00")
        self.assertEqual(result, 0.0)

    def test_convert_invalid_string(self):
        """Testa conversão de string inválida"""
        result = convert_string_to_float("abc123")
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
