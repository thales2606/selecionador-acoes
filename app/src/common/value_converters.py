"""Utilitários para conversão de valores"""

import re
import logging

logger = logging.getLogger(__name__)


def convert_string_to_float(value: str | float | None) -> float | None:
    """
    Converte string de valor monetário brasileiro para float.
    
    Formatos suportados:
    - "1.234.567,89" → 1234567.89
    - "1234567,89" → 1234567.89
    - "-123,45" → -123.45
    - "" → None
    - None → None
    
    Args:
        value: String, float ou None contendo o valor
        
    Returns:
        float ou None se conversão for bem-sucedida, None caso contrário
    """
    # Se já é float, retorna direto
    if isinstance(value, float):
        return value
    
    # Se é None ou vazio, retorna None
    if value is None or (isinstance(value, str) and value.strip() == ""):
        return None
    
    # Se não é string neste ponto, tenta converter para string
    if not isinstance(value, str):
        try:
            value = str(value).strip()
        except Exception as e:
            logger.warning(f"Erro ao converter valor para string: {value}, erro: {e}")
            return None
    
    try:
        # Remove espaços em branco
        value = value.strip()
        
        # Se continua vazio após strip
        if not value:
            return None
        
        # Remove símbolos de moeda e caracteres especiais (R$, $, €, etc.)
        value = re.sub(r'[^\d.,\-]', '', value)

        # Se continua vazio após remover caracteres especiais
        if not value:
            return None

        # Substitui ponto por nada (remove separador de milhares)
        # Substitui vírgula por ponto (converte decimal brasileiro para inglês)
        # Ordem é importante: primeiro remove ponto, depois substitui vírgula
        value_normalized = value.replace(".", "").replace(",", ".")
        
        # Converte para float
        result = float(value_normalized)
        return result
    except (ValueError, AttributeError) as e:
        logger.warning(f"Erro ao converter valor '{value}' para float: {e}")
        return None
