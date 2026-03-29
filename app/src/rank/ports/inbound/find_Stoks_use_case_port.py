from abc import ABC, abstractmethod
from typing import List


class FindStoksUseCasePort(ABC):
    """Interface de caso de uso para buscar stocks"""

    @abstractmethod
    def execute(self):
        """Busca e retorna a lista de stocks filtrados"""
        pass