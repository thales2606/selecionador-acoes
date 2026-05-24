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
from src.domain.services.stock_ranking_service import StockRankingService
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
                 details_invest_site_adapter: DetailsPageScrapingPort,
                 details_invest_10_adapter: DetailsPageScrapingPort,
                 repository: StockRepositoryPort,
                 extraction_service: StockExtractionService,
                 filter_service: StockFilterService,
                 ranking_service: StockRankingService,
                 volatility_service: StockVolatilityService = None
                 ):
        self._invest_adapter = invest_adapter
        self._financial_adapter = financial_adapter
        self._details_invest_site_adapter = details_invest_site_adapter
        self._details_invest_10_adapter = details_invest_10_adapter
        self._repository = repository
        self._extraction_service = extraction_service
        self._filter_service = filter_service
        self._ranking_service = ranking_service
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
        
        # REORDENADO: Enriquecimento ANTES dos filtros
        df_enriched = self._enrich_with_details(df_with_volatility)
        
        # Aplica filtros agora com dados enriquecidos
        df_filtered = self._apply_filters(df_enriched)
        
        # Calcula indicadores de ranking
        df_ranked = self._apply_ranking(df_filtered)
        
        # Salva resultados
        self._save_results(df_ranked)

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

        # Reseta o índice para garantir que fique sequencial (0, 1, 2, ...)
        df_reset = df.reset_index(drop=True)

        # Inicializa listas para armazenar os detalhes
        details_list = []

        # Itera sobre cada ação e faz o scraping dos detalhes
        for idx, row in df_reset.iterrows():
            stock_code = row.iloc[0]  # Primeira coluna contém o código da ação
            # if row['Financeira'] != 'Sim':
            #     continue
            details = self._scrape_details_page(stock_code, row['Financeira'] == 'Sim')
            details_list.append(details)
            print(f"Detalhes obtidos para {stock_code}")
            time.sleep(1)

        # Cria um dataframe com os detalhes
        df_details = pd.DataFrame(details_list)

        # Concatena as colunas de detalhes ao dataframe original usando índices alinhados
        df_enriched = pd.concat([df_reset, df_details], axis=1)

        print("Detalhes adicionados ao resultado!")
        return df_enriched

    def _scrape_details_page(self, stock_code: str, financial: bool) -> dict:
        invest_site_details = self._details_invest_site_adapter.scrape_details_page(stock_code, financial)
        invest_10_details = self._details_invest_10_adapter.scrape_details_page(stock_code, financial)
        return {
            'lucro_liquido_anual': invest_10_details['lucro_liquido_anual'],
            'lucro_liquido_trimestral': invest_10_details['lucro_liquido_trimestral'],
            'patrimonio_liquido': invest_10_details['patrimonio_liquido'],
            'situacao_empresa': invest_site_details['situacao_empresa'],
            'imposto_anual': invest_10_details['imposto_anual'],
            'imposto_trimestral': invest_10_details['imposto_trimestral']
        }

    def _save_results(self, df: pd.DataFrame) -> None:
        """Salva os resultados em um arquivo Excel"""
        print(f"Salvando resultados em {OUTPUT_FILE}...")
        self._repository.save_dataframe(df=df, file_path=OUTPUT_FILE, sheet_name=OUTPUT_SHEET)
        print("Salvamento concluído com sucesso!")

    def _apply_ranking(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calcula indicadores de ranking"""
        print("Calculando indicadores de ranking...")
        df_ranked = self._ranking_service.calculate_ranking_indicators(df)
        print("Indicadores de ranking calculados com sucesso!")
        return df_ranked
