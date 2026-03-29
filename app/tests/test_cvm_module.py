import unittest
from datetime import datetime
from unittest.mock import Mock

from src.rank.application.dto.cvm_company_output_dto import CVMCompanyOutputDTO, CVMFinancialDataOutputDTO
from src.domain.services.cvm_processing_service import CVMProcessingService
from src.rank.application.import_cvm_data_use_case import ImportCVMDataUseCase


class TestCVMCompanyOutputDTO(unittest.TestCase):
    """Testes para o DTO de empresa"""

    def test_create_company_dto(self):
        """Testa criação de DTO de empresa"""
        company = CVMCompanyOutputDTO(
            cvm_code="12345",
            cnpj="00.000.000/0000-00",
            company_name="Test Company"
        )

        self.assertEqual(company.cvm_code, "12345")
        self.assertEqual(company.cnpj, "00.000.000/0000-00")
        self.assertEqual(company.company_name, "Test Company")
        self.assertEqual(company.status, "ACTIVE")
        self.assertIsNotNone(company.created_at)


class TestCVMFinancialDataOutputDTO(unittest.TestCase):
    """Testes para o DTO de dados financeiros"""

    def test_create_financial_data_dto(self):
        """Testa criação de DTO de dados financeiros"""
        fin_data = CVMFinancialDataOutputDTO(
            cvm_code="12345",
            reference_date=datetime(2023, 12, 31),
            fiscal_year=2023,
            total_assets=1000000.00,
            revenue=500000.00
        )

        self.assertEqual(fin_data.cvm_code, "12345")
        self.assertEqual(fin_data.fiscal_year, 2023)
        self.assertEqual(fin_data.total_assets, 1000000.00)
        self.assertEqual(fin_data.revenue, 500000.00)


class TestCVMProcessingService(unittest.TestCase):
    """Testes para o serviço de processamento CVM"""

    def test_process_companies_data(self):
        """Testa processamento de dados de empresas"""
        raw_data = [
            {
                'CD_CVM': '12345',
                'CNPJ_CIA': '00.000.000/0000-00',
                'DENOM_CIA': 'Test Company 1',
                'SETOR': 'Finance',
                'SUBSETOR': 'Banking',
                'SEGMENTO': 'Shares'
            },
            {
                'CD_CVM': '67890',
                'CNPJ_CIA': '11.111.111/1111-11',
                'DENOM_CIA': 'Test Company 2',
                'SETOR': 'Tech',
            }
        ]

        companies = CVMProcessingService.process_companies_data(raw_data)

        self.assertEqual(len(companies), 2)
        self.assertEqual(companies[0].cvm_code, '12345')
        self.assertEqual(companies[0].company_name, 'Test Company 1')
        self.assertEqual(companies[1].cvm_code, '67890')

    def test_process_financial_data(self):
        """Testa processamento de dados financeiros"""
        raw_data = [
            {
                'CD_CVM': '12345',
                'DT_REFER': '2023-12-31',
                'VL_ATIVO': '1000000.00',
                'VL_ATIVO_CIRCULANTE': '500000.00',
                'VL_PASSIVO': '600000.00',
                'VL_PATRIMONIO_LIQUIDO': '400000.00',
                'VL_RECEITA_LIQUIDA': '800000.00',
                'VL_RESULTADO_LIQUIDO': '100000.00'
            }
        ]

        financial_data = CVMProcessingService.process_financial_data(raw_data, "DFP")

        self.assertEqual(len(financial_data), 1)
        self.assertEqual(financial_data[0].cvm_code, '12345')
        self.assertEqual(financial_data[0].fiscal_year, 2023)
        self.assertEqual(financial_data[0].total_assets, 1000000.00)

    def test_deduplicate_companies(self):
        """Testa remoção de duplicatas"""
        companies = [
            CVMCompanyOutputDTO(cvm_code="1", cnpj="a", company_name="A"),
            CVMCompanyOutputDTO(cvm_code="2", cnpj="b", company_name="B"),
            CVMCompanyOutputDTO(cvm_code="1", cnpj="c", company_name="C"),  # Duplicata
        ]

        dedup = CVMProcessingService.deduplicate_companies(companies)

        self.assertEqual(len(dedup), 2)
        self.assertEqual(dedup[0].cvm_code, "1")
        self.assertEqual(dedup[1].cvm_code, "2")


class TestImportCVMDataUseCase(unittest.TestCase):
    """Testes para o caso de uso de importação"""

    def setUp(self):
        """Configura mocks para os testes"""
        self.mock_scraping = Mock()
        self.mock_repository = Mock()
        self.use_case = ImportCVMDataUseCase(self.mock_scraping, self.mock_repository)

    def test_import_companies_success(self):
        """Testa importação bem-sucedida de empresas"""
        raw_data = [
            {
                'CD_CVM': '12345',
                'CNPJ_CIA': '00.000.000/0000-00',
                'DENOM_CIA': 'Test Company',
            }
        ]

        self.mock_scraping.download_companies_data.return_value = raw_data

        self.use_case.import_companies()

        self.mock_scraping.download_companies_data.assert_called_once()
        self.mock_repository.save_companies_batch.assert_called_once()

    def test_import_annual_reports_success(self):
        """Testa importação bem-sucedida de DFP"""
        raw_data = [
            {
                'CD_CVM': '12345',
                'DT_REFER': '2023-12-31',
                'VL_ATIVO': '1000000.00',
            }
        ]

        self.mock_scraping.download_financial_data.return_value = raw_data

        self.use_case.import_annual_reports(2023)

        self.mock_scraping.download_financial_data.assert_called_once_with(2023, "DFP")
        self.mock_repository.save_financial_data_batch.assert_called_once()


if __name__ == '__main__':
    unittest.main()

