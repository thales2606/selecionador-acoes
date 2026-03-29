from typing import List, Optional
from datetime import datetime
import logging

from src.rank.application.dto.cvm_company_output_dto import CVMCompanyOutputDTO, CVMFinancialDataOutputDTO

logger = logging.getLogger(__name__)


class CVMProcessingService:
    """Serviço para processar e transformar dados da CVM"""

    @staticmethod
    def process_companies_data(raw_data: List[dict]) -> List[CVMCompanyOutputDTO]:
        """
        Processa dados brutos de empresas da CVM em DTOs

        Args:
            raw_data: Lista de dicionários com dados brutos da CVM

        Returns:
            Lista de CVMCompanyOutputDTO
        """
        companies = []

        for row in raw_data:
            try:
                company = CVMCompanyOutputDTO(
                    cvm_code=str(row.get('CD_CVM', '')).strip(),
                    cnpj=str(row.get('CNPJ_CIA', '')).strip(),
                    company_name=str(row.get('DENOM_CIA', '')).strip(),
                    sector=str(row.get('SETOR', '')).strip() if row.get('SETOR') else None,
                    subsector=str(row.get('SUBSETOR', '')).strip() if row.get('SUBSETOR') else None,
                    segment=str(row.get('SEGMENTO', '')).strip() if row.get('SEGMENTO') else None,
                )
                companies.append(company)
            except Exception as e:
                logger.error(f"Erro ao processar empresa: {row}. Erro: {str(e)}")
                continue

        return companies

    @staticmethod
    def process_financial_data(
        raw_data: List[dict],
        document_type: str = "DFP"
    ) -> List[CVMFinancialDataOutputDTO]:
        """
        Processa dados brutos financeiros da CVM em DTOs

        Args:
            raw_data: Lista de dicionários com dados brutos da CVM
            document_type: Tipo de documento (DFP, ITR, FRE, FCA)

        Returns:
            Lista de CVMFinancialDataOutputDTO
        """
        financial_data = []

        for row in raw_data:
            try:
                # Parse date
                ref_date = CVMProcessingService._parse_date(row.get('DT_REFER'))

                # Extract year and quarter from date
                year = ref_date.year
                quarter = None
                if document_type == "ITR":
                    quarter = (ref_date.month - 1) // 3 + 1

                # Parse numeric values
                def parse_float(value) -> Optional[float]:
                    if value is None or value == '':
                        return None
                    try:
                        if isinstance(value, str):
                            return float(value.replace(',', '.'))
                        return float(value)
                    except (ValueError, AttributeError):
                        return None

                fin_data = CVMFinancialDataOutputDTO(
                    cvm_code=str(row.get('CD_CVM', '')).strip(),
                    reference_date=ref_date,
                    fiscal_year=year,
                    fiscal_quarter=quarter,
                    document_type=document_type,
                    total_assets=parse_float(row.get('VL_ATIVO', row.get('VL_ATIVO_TOTAL'))),
                    current_assets=parse_float(row.get('VL_ATIVO_CIRCULANTE')),
                    non_current_assets=parse_float(row.get('VL_ATIVO_NAO_CIRCULANTE')),
                    total_liabilities=parse_float(row.get('VL_PASSIVO', row.get('VL_PASSIVO_TOTAL'))),
                    current_liabilities=parse_float(row.get('VL_PASSIVO_CIRCULANTE')),
                    non_current_liabilities=parse_float(row.get('VL_PASSIVO_NAO_CIRCULANTE')),
                    shareholders_equity=parse_float(row.get('VL_PATRIMONIO_LIQUIDO', row.get('VL_PL'))),
                    revenue=parse_float(row.get('VL_RECEITA_LIQUIDA', row.get('VL_REC_OPERACIONAL'))),
                    gross_profit=parse_float(row.get('VL_LUCRO_BRUTO')),
                    operating_profit=parse_float(row.get('VL_RESULTADO_OPERACIONAL', row.get('VL_LUCRO_OPERACIONAL'))),
                    net_income=parse_float(row.get('VL_RESULTADO_LIQUIDO', row.get('VL_LUCRO_LIQUIDO'))),
                )
                financial_data.append(fin_data)
            except Exception as e:
                logger.error(f"Erro ao processar dado financeiro: {row}. Erro: {str(e)}")
                continue

        return financial_data

    @staticmethod
    def _parse_date(date_str: str) -> datetime:
        """Faz parse de data em formato string da CVM"""
        if isinstance(date_str, datetime):
            return date_str

        if isinstance(date_str, str):
            # Tenta diferentes formatos de data
            for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%Y%m%d']:
                try:
                    return datetime.strptime(date_str, fmt)
                except ValueError:
                    continue

        raise ValueError(f"Não foi possível fazer parse da data: {date_str}")

    @staticmethod
    def deduplicate_companies(companies: List[CVMCompanyOutputDTO]) -> List[CVMCompanyOutputDTO]:
        """Remove duplicatas de empresas mantendo o primeiro registro"""
        seen = set()
        result = []

        for company in companies:
            if company.cvm_code not in seen:
                seen.add(company.cvm_code)
                result.append(company)

        return result

