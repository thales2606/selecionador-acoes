# Exemplos de Uso - Selecionador de Ações

## 📚 Exemplos Práticos

### Exemplo 1: Execução Básica

**Arquivo: `app/main.py`**

```python
from dependency_injection import initialize_di
from src.rank.adapters.outbound.scraping.web_scraping_driver import WebScrapingDriver

def cleanup(ws: WebScrapingDriver) -> None:
    """Libera recursos"""
    if ws:
        ws.close()

if __name__ == '__main__':
    # Inicializar injeção de dependências
    controller, web_scraping = initialize_di()
    
    try:
        # Executar scraping e filtragem
        controller.start_scraping()
        print("✓ Execução completada com sucesso!")
    
    except Exception as e:
        print(f"✗ Erro: {e}")
    
    finally:
        # Sempre liberar recursos (fechar browser)
        cleanup(web_scraping)
```

**Como executar:**
```powershell
python app/main.py
```

---

### Exemplo 2: Execução com Debug

Para ver o navegador em ação e debug:

**Arquivo: `app/debug_main.py`**

```python
import logging
from dependency_injection import initialize_di
from src.rank.adapters.outbound.scraping.web_scraping_driver import WebScrapingDriver
from src.common.constants import WEBDRIVER_HEADLESS, WAIT_TIME_AFTER_FILTER

# Configurar logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def main():
    logger.info(f"Iniciando com headless={WEBDRIVER_HEADLESS}, timeout={WAIT_TIME_AFTER_FILTER}s")
    
    controller, web_scraping = initialize_di()
    
    try:
        controller.start_scraping()
        logger.info("✓ Execução completada")
    
    except Exception as e:
        logger.error(f"✗ Erro: {e}", exc_info=True)
    
    finally:
        if web_scraping:
            web_scraping.close()
        logger.info("Recursos liberados")

if __name__ == '__main__':
    main()
```

**Como executar:**
```powershell
# Será criado app.log com detalhes
python app/debug_main.py

# Ver logs em tempo real:
Get-Content app.log -Tail 20
```

---

### Exemplo 3: Usar Adapters Individuais

Para testar um adapter isoladamente:

**Arquivo: `app/test_single_adapter.py`**

```python
from src.rank.adapters.outbound.scraping.web_scraping_driver import WebScrapingDriver
from src.rank.adapters.outbound.scraping.invest_site_scraping_adapter import InvestSiteScrapingAdapter

def test_non_financial_adapter():
    """Testa adapter de ações não-financeiras"""
    
    web_driver = WebScrapingDriver()
    
    try:
        # Criar adapter
        adapter = InvestSiteScrapingAdapter(web_driver)
        
        print("1. Aplicando filtros...")
        adapter.apply_filters()
        
        print("2. Obtendo resultados...")
        html_content = adapter.get_results_table()
        
        print(f"3. HTML obtido: {len(html_content)} caracteres")
        
        # Verificar se tem tabela
        if '<table' in html_content:
            print("✓ Tabela encontrada!")
        else:
            print("✗ Tabela não encontrada")
    
    finally:
        web_driver.close()

if __name__ == '__main__':
    test_non_financial_adapter()
```

**Como executar:**
```powershell
python app/test_single_adapter.py
```

---

### Exemplo 4: Processar Dados com Serviços

Para testar serviços de domínio isoladamente:

**Arquivo: `app/test_services.py`**

```python
import pandas as pd
from src.domain.services.stock_filter_service import StockFilterService
from src.domain.services.stock_extraction_service import StockExtractionService

def test_extraction_and_filtering():
    """Testa extração e filtragem de ações"""
    
    # Dados de exemplo (resultado do scraping)
    sample_html = """
    <table>
        <tr>
            <td>PETR4</td>
            <td>12.5</td>
            <td>15.2</td>
            <td>3.5</td>
            <td>8.2</td>
            <td>5000000</td>
        </tr>
        <tr>
            <td>VALE3</td>
            <td>14.1</td>
            <td>18.9</td>
            <td>2.8</td>
            <td>6.5</td>
            <td>6000000</td>
        </tr>
    </table>
    """
    
    # 1. Testar extração
    print("=== TESTE DE EXTRAÇÃO ===")
    extraction_service = StockExtractionService()
    df = extraction_service.extract_from_html(sample_html, financial=False)
    print(f"Ações extraídas: {len(df)}")
    print(df)
    
    # 2. Testar filtragem
    print("\n=== TESTE DE FILTRAGEM ===")
    filter_service = StockFilterService()
    df_filtered = filter_service.apply_all_filters(df)
    print(f"Ações após filtros: {len(df_filtered)}")
    print(df_filtered)

if __name__ == '__main__':
    test_extraction_and_filtering()
```

**Como executar:**
```powershell
python app/test_services.py
```

---

### Exemplo 5: Calcular Volatilidade

Para testar cálculo de volatilidade:

**Arquivo: `app/test_volatility.py`**

```python
import pandas as pd
from src.domain.services.stock_volatility_service import StockVolatilityService
from src.common.constants import VOLATILITY_PERIOD, VOLATILITY_BATCH_SIZE, VOLATILITY_DELAY_BETWEEN_BATCHES

def test_volatility():
    """Testa cálculo de volatilidade"""
    
    # Criar dataframe com alguns tickers
    df = pd.DataFrame({
        'Ticker': ['PETR4', 'VALE3', 'WEGE3'],
        'ROI': [12.5, 14.1, 16.8],
        'Volume': [5000000, 6000000, 4000000]
    })
    
    print(f"Tickers para calcular volatilidade: {df['Ticker'].tolist()}")
    print(f"Período: {VOLATILITY_PERIOD}")
    
    # Criar serviço
    volatility_service = StockVolatilityService(
        period=VOLATILITY_PERIOD,
        batch_size=VOLATILITY_BATCH_SIZE,
        delay_between_batches=VOLATILITY_DELAY_BETWEEN_BATCHES
    )
    
    # Calcular volatilidade
    print("\nCalculando volatilidade...")
    df_with_volatility = volatility_service.calculate_volatility(df)
    
    print("\n=== RESULTADOS ===")
    print(df_with_volatility[['Ticker', 'Volatilidade']])

if __name__ == '__main__':
    test_volatility()
```

**Como executar:**
```powershell
# Pode levar alguns minutos (requisições ao yfinance)
python app/test_volatility.py
```

---

### Exemplo 6: Criar Mock para Testes Unitários

Para criar testes sem dependências externas:

**Arquivo: `app/test_with_mocks.py`**

```python
from unittest.mock import Mock, patch
import pandas as pd
from src.rank.application.find_stoks_use_case import FindStoksUseCase
from src.domain.services.stock_extraction_service import StockExtractionService
from src.domain.services.stock_filter_service import StockFilterService
from src.domain.services.stock_volatility_service import StockVolatilityService

class MockWebScrapingAdapter:
    """Mock para adapter de scraping"""
    
    def apply_filters(self):
        pass
    
    def get_results_table(self) -> str:
        # Retorna HTML de exemplo
        return "<table><tr><td>PETR4</td></tr></table>"

class MockStockRepository:
    """Mock para repositório"""
    
    def __init__(self):
        self.saved_data = None
    
    def save(self, stocks: pd.DataFrame) -> None:
        self.saved_data = stocks

def test_use_case_with_mocks():
    """Testa caso de uso sem dependências externas"""
    
    # Criar mocks
    mock_invest_adapter = MockWebScrapingAdapter()
    mock_financial_adapter = MockWebScrapingAdapter()
    mock_details_invest_adapter = Mock()
    mock_details_invest10_adapter = Mock()
    mock_repository = MockStockRepository()
    
    extraction_service = StockExtractionService()
    filter_service = StockFilterService()
    volatility_service = StockVolatilityService()
    
    # Criar caso de uso
    use_case = FindStoksUseCase(
        invest_adapter=mock_invest_adapter,
        financial_adapter=mock_financial_adapter,
        details_invest_site_adapter=mock_details_invest_adapter,
        details_invest_10_adapter=mock_details_invest10_adapter,
        repository=mock_repository,
        extraction_service=extraction_service,
        filter_service=filter_service,
        volatility_service=volatility_service
    )
    
    # Executar (com dados de mock)
    print("Executando caso de uso com mocks...")
    # use_case.execute()
    
    # Verificar se dados foram salvos
    if mock_repository.saved_data is not None:
        print(f"✓ {len(mock_repository.saved_data)} ações salvas")
        print(mock_repository.saved_data.head())
    else:
        print("✗ Nenhuma dado salvo")

if __name__ == '__main__':
    test_use_case_with_mocks()
```

**Como executar:**
```powershell
python app/test_with_mocks.py
```

---

### Exemplo 7: Salvar em Excel com Formatação

Para customizar o salvamento em Excel:

**Arquivo: `app/save_with_formatting.py`**

```python
import pandas as pd
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils.dataframe import dataframe_to_rows
from src.common.constants import OUTPUT_FILE, OUTPUT_SHEET

def save_with_formatting(df: pd.DataFrame):
    """Salva DataFrame em Excel com formatação"""
    
    from openpyxl import Workbook
    
    wb = Workbook()
    ws = wb.active
    ws.title = OUTPUT_SHEET
    
    # Escrever dados
    for r_idx, row in enumerate(dataframe_to_rows(df, index=False, header=True), 1):
        for c_idx, value in enumerate(row, 1):
            cell = ws.cell(row=r_idx, column=c_idx)
            cell.value = value
            
            # Formatar header
            if r_idx == 1:
                cell.font = Font(bold=True, color="FFFFFF")
                cell.fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
                cell.alignment = Alignment(horizontal="center", vertical="center")
            
            # Alinhar numbers à direita
            if isinstance(value, (int, float)):
                cell.alignment = Alignment(horizontal="right")
    
    # Auto-ajustar largura das colunas
    for column in ws.columns:
        max_length = 0
        column_letter = column[0].column_letter
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = min(max_length + 2, 50)
        ws.column_dimensions[column_letter].width = adjusted_width
    
    # Congelar header
    ws.freeze_panes = "A2"
    
    # Salvar
    wb.save(OUTPUT_FILE)
    print(f"✓ Arquivo salvo com formatação em: {OUTPUT_FILE}")

# Exemplo de uso
if __name__ == '__main__':
    # Criar dataframe de exemplo
    df = pd.DataFrame({
        'Ticker': ['PETR4', 'VALE3', 'WEGE3'],
        'ROI': [12.5, 14.1, 16.8],
        'Volatilidade': [0.35, 0.42, 0.28],
        'Volume': [5000000, 6000000, 4000000]
    })
    
    save_with_formatting(df)
```

**Como executar:**
```powershell
python app/save_with_formatting.py
```

---

### Exemplo 8: Analisar Resultados

Para analisar os resultados gerados:

**Arquivo: `app/analyze_results.py`**

```python
import pandas as pd
from src.common.constants import OUTPUT_FILE, OUTPUT_SHEET

def analyze_results():
    """Analisa o arquivo Excel gerado"""
    
    try:
        # Ler Excel
        df = pd.read_excel(OUTPUT_FILE, sheet_name=OUTPUT_SHEET)
        
        print(f"=== ANÁLISE DE RESULTADOS ===")
        print(f"\nTotal de ações: {len(df)}")
        
        # Estatísticas por coluna
        print("\n=== ESTATÍSTICAS ===")
        print(df.describe())
        
        # Top 10 por ROI (se existir coluna)
        if 'ROI' in df.columns:
            print("\n=== TOP 10 POR ROI ===")
            top_roi = df.nlargest(10, 'ROI')[['Ticker', 'ROI']]
            print(top_roi)
        
        # Top 10 por Volatilidade (se existir coluna)
        if 'Volatilidade' in df.columns:
            print("\n=== TOP 10 MENOR VOLATILIDADE ===")
            low_vol = df.nsmallest(10, 'Volatilidade')[['Ticker', 'Volatilidade']]
            print(low_vol)
        
        # Setor com mais ações (se existir coluna)
        if 'Setor' in df.columns:
            print("\n=== AÇÕES POR SETOR ===")
            by_setor = df['Setor'].value_counts()
            print(by_setor)
        
    except FileNotFoundError:
        print(f"✗ Arquivo não encontrado: {OUTPUT_FILE}")
    except Exception as e:
        print(f"✗ Erro ao analisar: {e}")

if __name__ == '__main__':
    analyze_results()
```

**Como executar:**
```powershell
python app/analyze_results.py
```

---

### Exemplo 9: Executar Apenas Scraping Não-Financeiro

Para scraping seletivo:

**Arquivo: `app/scrape_non_financial_only.py`**

```python
from src.rank.adapters.outbound.scraping.web_scraping_driver import WebScrapingDriver
from src.rank.adapters.outbound.scraping.invest_site_scraping_adapter import InvestSiteScrapingAdapter
from src.domain.services.stock_extraction_service import StockExtractionService
from src.common.constants import WAIT_TIME_AFTER_FILTER
import time

def scrape_non_financial_only():
    """Scraping apenas de ações não-financeiras"""
    
    web_driver = WebScrapingDriver()
    extraction_service = StockExtractionService()
    
    try:
        # Criar adapter
        adapter = InvestSiteScrapingAdapter(web_driver)
        
        # Aplicar filtros
        print("Aplicando filtros...")
        adapter.apply_filters()
        
        # Aguardar renderização
        print(f"Aguardando {WAIT_TIME_AFTER_FILTER} segundos...")
        time.sleep(WAIT_TIME_AFTER_FILTER)
        
        # Obter resultados
        print("Obtendo tabela de resultados...")
        html_content = adapter.get_results_table()
        
        # Extrair dados
        print("Extraindo dados...")
        df = extraction_service.extract_from_html(html_content, financial=False)
        
        print(f"\n✓ {len(df)} ações não-financeiras encontradas")
        print(df.head(10))
    
    finally:
        web_driver.close()

if __name__ == '__main__':
    scrape_non_financial_only()
```

**Como executar:**
```powershell
python app/scrape_non_financial_only.py
```

---

### Exemplo 10: Executar Apenas Scraping Financeiro

Para scraping apenas de ações financeiras:

**Arquivo: `app/scrape_financial_only.py`**

```python
from src.rank.adapters.outbound.scraping.web_scraping_driver import WebScrapingDriver
from src.rank.adapters.outbound.scraping.invest_site_financial_scraping_adapter import InvestSiteFinancialScrapingAdapter
from src.domain.services.stock_extraction_service import StockExtractionService
from src.common.constants import WAIT_TIME_AFTER_FILTER
import time

def scrape_financial_only():
    """Scraping apenas de ações financeiras"""
    
    web_driver = WebScrapingDriver()
    extraction_service = StockExtractionService()
    
    try:
        # Criar adapter
        adapter = InvestSiteFinancialScrapingAdapter(web_driver)
        
        # Aplicar filtros
        print("Aplicando filtros para ações financeiras...")
        adapter.apply_filters()
        
        # Aguardar renderização
        print(f"Aguardando {WAIT_TIME_AFTER_FILTER} segundos...")
        time.sleep(WAIT_TIME_AFTER_FILTER)
        
        # Obter resultados
        print("Obtendo tabela de resultados...")
        html_content = adapter.get_results_table()
        
        # Extrair dados
        print("Extraindo dados...")
        df = extraction_service.extract_from_html(html_content, financial=True)
        
        print(f"\n✓ {len(df)} ações financeiras encontradas")
        print(df.head(10))
    
    finally:
        web_driver.close()

if __name__ == '__main__':
    scrape_financial_only()
```

**Como executar:**
```powershell
python app/scrape_financial_only.py
```

---

## 🎯 Quick Reference

| Tarefa | Arquivo | Comando |
|--------|---------|---------|
| Execução normal | `main.py` | `python app/main.py` |
| Debug com logs | `debug_main.py` | `python app/debug_main.py` |
| Testar um adapter | `test_single_adapter.py` | `python app/test_single_adapter.py` |
| Testar serviços | `test_services.py` | `python app/test_services.py` |
| Calcular volatilidade | `test_volatility.py` | `python app/test_volatility.py` |
| Testar com mocks | `test_with_mocks.py` | `python app/test_with_mocks.py` |
| Salvar com formato | `save_with_formatting.py` | `python app/save_with_formatting.py` |
| Analisar resultados | `analyze_results.py` | `python app/analyze_results.py` |
| Apenas não-financeiro | `scrape_non_financial_only.py` | `python app/scrape_non_financial_only.py` |
| Apenas financeiro | `scrape_financial_only.py` | `python app/scrape_financial_only.py` |

---

## 💡 Dicas

1. **Usar `test_single_adapter.py`** para verificar se o scraping está funcionando
2. **Usar `debug_main.py`** quando algo não está funcionando (vê o browser em ação)
3. **Usar `test_with_mocks.py`** para testes unitários rápidos
4. **Usar `analyze_results.py`** após execução para verificar qualidade dos dados

---

Todos os exemplos funcionam de forma independente e podem ser modificados para suas necessidades!

