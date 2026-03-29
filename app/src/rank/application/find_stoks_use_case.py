import time

import pandas as pd

from src.common.constants import (
    WAIT_TIME_AFTER_FILTER,
    OUTPUT_FILE,
    OUTPUT_SHEET,
    VOLATILITY_PERIOD,
    VOLATILITY_BATCH_SIZE,
    VOLATILITY_DELAY_BETWEEN_BATCHES
)
from src.domain.services.stock_extraction_service import StockExtractionService
from src.domain.services.stock_filter_service import StockFilterService
from src.domain.services.stock_volatility_service import StockVolatilityService
from src.rank.adapters.outbound.scraping.invest_site_financial_scraping_adapter import \
    InvestSiteFinancialScrapingAdapter
from src.rank.ports.inbound.find_Stoks_use_case_port import FindStoksUseCasePort
from src.rank.ports.outbound.Invest_site_scraping_port import InvestSiteScrapingPort
from src.rank.ports.outbound.details_page_scraping_port import DetailsPageScrapingPort
from src.rank.ports.outbound.stock_repository_port import StockRepositoryPort


class FindStoksUseCase(FindStoksUseCasePort):
    """Caso de uso para buscar e filtrar stocks"""

    def __init__(self,
                 invest_adapter: InvestSiteScrapingPort,
                 financial_adapter: InvestSiteFinancialScrapingAdapter,
                 details_adapter: DetailsPageScrapingPort,
                 repository: StockRepositoryPort,
                 extraction_service: StockExtractionService,
                 filter_service: StockFilterService,
                 volatility_service: StockVolatilityService = None
                 ):
        self._invest_adapter = invest_adapter
        self._financial_adapter = financial_adapter
        self._details_adapter = details_adapter
        self._repository = repository
        self._extraction_service = extraction_service
        self._filter_service = filter_service
        self._volatility_service = volatility_service or StockVolatilityService(
            period=VOLATILITY_PERIOD,
            batch_size=VOLATILITY_BATCH_SIZE,
            delay_between_batches=VOLATILITY_DELAY_BETWEEN_BATCHES
        )

    def execute(self):
        """Executa o fluxo completo de scraping e filtragem"""
        # Não financeiras
        html_content = self._perform_scraping(False)
        df_non_financial = self._extraction_service.extract_from_html(html_content, False)

        # Financeiras
        html_content = self._perform_scraping(True)
        df_financial = self._extraction_service.extract_from_html(html_content, True)
        # Junta os dataframes
        df_combined = pd.concat([df_non_financial, df_financial], ignore_index=True)

        print(f"\nTotal de ações após juntar financeiras e não-financeiras: {len(df_combined)}")

        # Calcula volatilidade no dataframe combinado
        df_with_volatility = self._calculate_volatility(df_combined)
        df_with_volatility = self._apply_filters(df_with_volatility)
        df_with_volatility = self._enrich_with_details(df_with_volatility)
        self._save_results(df_with_volatility)

    def _perform_scraping(self, financials: bool) -> str:
        """Realiza o scraping no site investsite"""
        print("Aplicando filtros no site...")
        if financials:
            self._financial_adapter.apply_filters()
            time.sleep(WAIT_TIME_AFTER_FILTER)
            html_content = self._financial_adapter.get_results_table()
        else:
            self._invest_adapter.apply_filters()
            time.sleep(WAIT_TIME_AFTER_FILTER)
            html_content = self._invest_adapter.get_results_table()
        return html_content

    def _apply_filters(self, df: pd.DataFrame) -> pd.DataFrame:
        """Aplica os filtros de negócio aos dados"""
        print("Aplicando filtros de negócio...")
        df_filtered = self._filter_service.apply_all_filters(df)
        print(f"Total de ações após filtros: {len(df_filtered)}")
        return df_filtered

    def _calculate_volatility(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calcula a volatilidade anual das ações"""
        print("\nCalculando volatilidade das ações...")
        df_with_volatility = self._volatility_service.calculate_volatility(df)
        print("Volatilidade adicionada ao resultado!")
        return df_with_volatility

    def _enrich_with_details(self, df: pd.DataFrame) -> pd.DataFrame:
        """Scrapa detalhes de cada ação e adiciona como novas colunas"""
        print("\nCapturando detalhes das ações...")

        # Inicializa listas para armazenar os detalhes
        details_list = []

        # Itera sobre cada ação e faz o scraping dos detalhes
        for idx, row in df.iterrows():
            stock_code = row.iloc[0]  # Primeira coluna contém o código da ação
            details = self._details_adapter.scrape_details_page(stock_code)
            details_list.append(details)
            print(f"Detalhes obtidos para {stock_code}")
            time.sleep(1)

        # Cria um dataframe com os detalhes
        df_details = pd.DataFrame(details_list)

        # Concatena as colunas de detalhes ao dataframe original
        df_enriched = pd.concat([df, df_details], axis=1)

        print("Detalhes adicionados ao resultado!")
        return df_enriched

    def _save_results(self, df: pd.DataFrame) -> None:
        """Salva os resultados em um arquivo Excel"""
        print(f"Salvando resultados em {OUTPUT_FILE}...")
        self._repository.save_dataframe(df=df, file_path=OUTPUT_FILE, sheet_name=OUTPUT_SHEET)
        print("Salvamento concluído com sucesso!")

