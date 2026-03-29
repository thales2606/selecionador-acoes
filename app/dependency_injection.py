from src.common.constants import URL_INVESTSITE, URL_INVESTSITE_FINANCEIRAS, VOLATILITY_PERIOD, VOLATILITY_BATCH_SIZE, \
    VOLATILITY_DELAY_BETWEEN_BATCHES
from src.domain.services.stock_extraction_service import StockExtractionService
from src.domain.services.stock_filter_service import StockFilterService
from src.domain.services.stock_volatility_service import StockVolatilityService
from src.rank.adapters.inbound.start_scraping import StartScrapingController
from src.rank.adapters.outbound.database.excel_stock_repository import ExcelStockRepository
from src.rank.adapters.outbound.scraping.invest_site_details_page_scraping_adapter import \
    InvestSiteDetailsPageScrapingAdapter
from src.rank.adapters.outbound.scraping.invest_site_scraping_adapter import InvestSiteScrapingAdapter
from src.rank.adapters.outbound.scraping.invest_site_financial_scraping_adapter import InvestSiteFinancialScrapingAdapter
from src.rank.adapters.outbound.scraping.web_scraping_driver import WebScrapingDriver
from src.rank.application.find_stoks_use_case import FindStoksUseCase


def initialize_di() -> tuple[StartScrapingController, WebScrapingDriver]:
    """
    Inicializa todos os adapters necessários para scraping de ações

    Args:
        financial: Se True, busca ações de empresas financeiras. Se False, busca ações não-financeiras
    """
    web_scraping = WebScrapingDriver()
    financial_adapter = InvestSiteFinancialScrapingAdapter(web_scraping)
    invest_adapter = InvestSiteScrapingAdapter(web_scraping)
    details_adapter = InvestSiteDetailsPageScrapingAdapter(web_scraping)

    filter_service = StockFilterService()
    extraction_service = StockExtractionService()
    volatility_service = StockVolatilityService(
        period=VOLATILITY_PERIOD,
        batch_size=VOLATILITY_BATCH_SIZE,
        delay_between_batches=VOLATILITY_DELAY_BETWEEN_BATCHES
    )
    repository = ExcelStockRepository()
    use_case = FindStoksUseCase(
        invest_adapter,
        financial_adapter,
        details_adapter,
        repository,
        extraction_service,
        filter_service,
        volatility_service
    )
    return StartScrapingController(use_case), web_scraping
