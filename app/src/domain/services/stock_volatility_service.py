import time
import pandas as pd
import yfinance as yf
import numpy as np
from typing import List


class StockVolatilityService:
    """Serviço para calcular a volatilidade anual das ações usando yfinance"""

    def __init__(self,
                 period: str = "1y",
                 batch_size: int = 5,
                 delay_between_batches: float = 1.0):
        """
        Inicializa o serviço de volatilidade

        Args:
            period: Período de análise (padrão: "1y" para 1 ano)
            batch_size: Quantidade de ações por requisição (padrão: 5)
            delay_between_batches: Delay em segundos entre requisições (padrão: 1.0)
        """
        self.period = period
        self.batch_size = batch_size
        self.delay_between_batches = delay_between_batches

    def calculate_volatility(self, df: pd.DataFrame, ticker_column: str = 'Ação') -> pd.DataFrame:
        """
        Calcula a volatilidade anual para todas as ações

        Args:
            df: DataFrame com as ações
            ticker_column: Nome da coluna que contém os tickers

        Returns:
            DataFrame com a coluna de volatilidade adicionada
        """
        df = df.copy()
        tickers = df[ticker_column].tolist()

        print(f"Iniciando cálculo de volatilidade para {len(tickers)} ações...")
        print(f"Configuração: período={self.period}, batch_size={self.batch_size}")

        volatilities = self._fetch_volatilities_in_batches(tickers)

        df['Volatilidade Anual (%)'] = df[ticker_column].map(volatilities)

        print(f"Volatilidade calculada com sucesso!")
        return df

    def _fetch_volatilities_in_batches(self, tickers: List[str]) -> dict:
        """
        Busca volatilidades em lotes para não sobrecarregar o servidor

        Args:
            tickers: Lista de tickers

        Returns:
            Dicionário com ticker -> volatilidade
        """
        volatilities = {}
        total_batches = (len(tickers) + self.batch_size - 1) // self.batch_size

        for i in range(0, len(tickers), self.batch_size):
            batch_num = (i // self.batch_size) + 1
            batch = tickers[i:i + self.batch_size]

            print(f"Processando lote {batch_num}/{total_batches}: {', '.join(batch)}")

            batch_volatilities = self._calculate_batch_volatility(batch)
            # Manter a chave do dicionário sem .SA (ticker original)
            volatilities.update(batch_volatilities)

            # Aguarda entre os lotes para não sobrecarregar o servidor
            if i + self.batch_size < len(tickers):
                print(f"Aguardando {self.delay_between_batches}s antes do próximo lote...")
                time.sleep(self.delay_between_batches)

        return volatilities

    def _calculate_batch_volatility(self, tickers: List[str]) -> dict:
        """
        Calcula volatilidade para um lote de tickers

        Args:
            tickers: Lista de tickers para este lote

        Returns:
            Dicionário com ticker -> volatilidade
        """
        result = {}

        try:
            # Adiciona .SA aos tickers para buscar no yfinance
            tickers_with_suffix = [f"{ticker}.SA" for ticker in tickers]

            # Baixa dados de preço para o período especificado
            dados = yf.download(tickers_with_suffix, period=self.period, progress=False)["Close"]

            # Se for apenas um ticker, yfinance retorna uma Series ao invés de DataFrame
            if isinstance(dados, pd.Series):
                dados = dados.to_frame(name=tickers_with_suffix[0])

            # Calcula retornos logarítmicos
            retornos = np.log(dados / dados.shift(1))

            # Calcula volatilidade diária e anualiza (252 dias úteis)
            vol_diaria = retornos.std()
            vol_anual = vol_diaria * np.sqrt(252)

            # Converte para percentual
            for ticker, ticker_with_suffix in zip(tickers, tickers_with_suffix):
                if ticker_with_suffix in vol_anual.index:
                    volatility_pct = vol_anual[ticker_with_suffix] * 100
                    result[ticker] = round(volatility_pct, 2)
                else:
                    result[ticker] = None
                    print(f"⚠️  Não foi possível calcular volatilidade para {ticker}")

        except Exception as e:
            print(f"❌ Erro ao calcular volatilidade para lote {tickers}: {str(e)}")
            for ticker in tickers:
                result[ticker] = None

        return result

