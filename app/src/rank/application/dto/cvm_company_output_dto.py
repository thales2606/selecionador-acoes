from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class CVMCompanyOutputDTO:
    """DTO para dados de empresa da CVM"""
    cvm_code: str
    cnpj: str
    company_name: str
    sector: Optional[str] = None
    subsector: Optional[str] = None
    segment: Optional[str] = None
    status: str = "ACTIVE"
    created_at: datetime = None
    updated_at: datetime = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()


@dataclass
class CVMFinancialDataOutputDTO:
    """DTO para dados financeiros da CVM"""
    cvm_code: str
    reference_date: datetime
    fiscal_year: int
    fiscal_quarter: Optional[int] = None
    document_type: str = "DFP"  # DFP, ITR, FRE, FCA

    # Balanço Patrimonial Ativo
    total_assets: Optional[float] = None
    current_assets: Optional[float] = None
    non_current_assets: Optional[float] = None

    # Balanço Patrimonial Passivo
    total_liabilities: Optional[float] = None
    current_liabilities: Optional[float] = None
    non_current_liabilities: Optional[float] = None

    # Patrimônio Líquido
    shareholders_equity: Optional[float] = None

    # Demonstração de Resultado
    revenue: Optional[float] = None
    gross_profit: Optional[float] = None
    operating_profit: Optional[float] = None
    net_income: Optional[float] = None

    created_at: datetime = None
    updated_at: datetime = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()

