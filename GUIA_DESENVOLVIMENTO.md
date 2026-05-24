# Guia de Desenvolvimento - Selecionador de Ações

## 📖 Índice
1. [Estrutura do Projeto](#estrutura-do-projeto)
2. [Fluxo de Dados](#fluxo-de-dados)
3. [Como Adicionar Novos Componentes](#como-adicionar-novos-componentes)
4. [Testabilidade](#testabilidade)
5. [Troubleshooting](#troubleshooting)

## Estrutura do Projeto

### Diretório: `src/common/`

**Responsabilidade**: Configurações e constantes compartilhadas

**Arquivo Principal: `constants.py`**
```python
# URLs dos sites
URL_INVESTSITE = "https://www.investsite.com.br/seleciona_acoes.php"
URL_INVESTSITE_FINANCEIRAS = "https://www.investsite.com.br/seleciona_acoes_financ.php"

# Arquivo de saída
OUTPUT_FILE = r'C:\Users\thale\OneDrive\Finanças\rancking_acoes_brasileiras.xlsx'

# Parâmetros de scraping
WAIT_TIME_AFTER_FILTER = 35  # Tempo de espera para renderizar resultados
VOLUME_MINIMO = '3000000'
```

**Como modificar:**
- Para mudar a pasta de saída, editar `OUTPUT_FILE`
- Para ajustar timeouts, editar `WAIT_TIME_AFTER_FILTER`
- Para alterar filtros padrão, editar `VOLUME_MINIMO`, `MARGEM_EBIT_MINIMO`

---

### Diretório: `src/domain/`

**Responsabilidade**: Lógica de negócio pura (independente de frameworks)

#### `services/stock_extraction_service.py`
```python
class StockExtractionService:
    """
    Extrai dados estruturados do HTML retornado pelos adapters
    
    Responsabilidades:
    - Fazer parsing do HTML
    - Extrair tabelas de ações
    - Converter para DataFrame
    - Normalizar dados (tipos, formatos)
    """
    
    def extract_from_html(self, html_content: str, financial: bool) -> pd.DataFrame:
        """
        Args:
            html_content: HTML da tabela de ações
            financial: True para ações financeiras, False para não-financeiras
        
        Returns:
            DataFrame com colunas padronizadas
        """
```

**Colunas esperadas:**
- Para não-financeiras: `['Ticker', 'ROI', 'Margem EBIT', 'EV/EBIT', 'DY', 'Volume', 'Market Cap']`
- Para financeiras: `['Ticker', 'ROE', 'Margem Líquida', 'Alavancagem', 'P/E', 'P/B', 'DY', 'Volume', 'Market Cap']`

#### `services/stock_filter_service.py`
```python
class StockFilterService:
    """
    Aplica regras de filtragem de negócio aos dados
    
    Filtros aplicados (em ordem):
    1. Remove seguradoras (SUL AMÉRICA, PORTO SEGURO)
    2. Remove BDRs (tickers com '33')
    3. Remove duplicatas (mantém maior volume)
    4. Remove valores nulos em colunas críticas
    5. Ordena por EV/EBIT (para não-financeiras)
    """
    
    def apply_all_filters(self, df: pd.DataFrame) -> pd.DataFrame:
        """Aplica todos os filtros em sequência"""
```

#### `services/stock_volatility_service.py`
```python
class StockVolatilityService:
    """
    Calcula volatilidade anual das ações usando dados históricos
    
    Parâmetros:
    - period: "1y" para 1 ano de dados
    - batch_size: Quantidade de ações por requisição ao yfinance
    - delay_between_batches: Delay em segundos entre requisições
    """
    
    def calculate_volatility(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcula volatilidade e adiciona coluna 'Volatilidade'
        
        Nota: Executa requisições ao yfinance, pode levar alguns minutos
        """
```

---

### Diretório: `src/rank/ports/`

**Responsabilidade**: Definir contratos (interfaces) para componentes externos

#### `inbound/find_Stoks_use_case_port.py`
```python
class FindStoksUseCasePort(ABC):
    """Interface que define o contrato do caso de uso"""
    
    @abstractmethod
    def execute(self):
        """Executa o fluxo completo de scraping"""
```

#### `outbound/Invest_site_scraping_port.py`
```python
class InvestSiteScrapingPort(ABC):
    """Interface para adapters de web scraping"""
    
    @abstractmethod
    def apply_filters(self):
        """Aplica filtros no site"""
    
    @abstractmethod
    def get_results_table(self) -> str:
        """Retorna HTML da tabela de resultados"""
```

#### `outbound/details_page_scraping_port.py`
```python
class DetailsPageScrapingPort(ABC):
    """Interface para scraping de detalhes de ações individuais"""
    
    @abstractmethod
    def get_details(self, ticker: str) -> dict:
        """Retorna detalhes técnicos da ação"""
```

#### `outbound/stock_repository_port.py`
```python
class StockRepositoryPort(ABC):
    """Interface para persistência de ações"""
    
    @abstractmethod
    def save(self, stocks: pd.DataFrame) -> None:
        """Salva ações em repositório (Excel, BD, etc.)"""
```

**Como criar nova interface:**
1. Criar arquivo em `src/rank/ports/outbound/`
2. Herdar de `ABC`
3. Definir métodos com `@abstractmethod`
4. Documentar parâmetros e retorno

---

### Diretório: `src/rank/adapters/`

**Responsabilidade**: Implementações concretas das interfaces

#### `outbound/scraping/web_scraping_driver.py`

```python
class WebScrapingDriver:
    """Encapsula Selenium WebDriver para Firefox"""
    
    def __init__(self):
        self.driver = webdriver.Firefox(...)
    
    def navigate_to(self, url: str):
        """Navega para URL"""
    
    def click_element(self, xpath: str):
        """Clica em elemento via XPath"""
    
    def get_element_html(self, xpath: str) -> str:
        """Retorna HTML do elemento"""
    
    def close(self):
        """Fecha browser"""
```

#### `outbound/scraping/invest_site_scraping_adapter.py`

```python
class InvestSiteScrapingAdapter(InvestSiteScrapingPort):
    """Adapter para scraping de ações não-financeiras"""
    
    def __init__(self, web_driver: WebScrapingDriver):
        self.web_driver = web_driver
        self.url = URL_INVESTSITE
    
    def apply_filters(self):
        """
        Aplica filtros no site InvestSite
        
        Passos:
        1. Navega para URL
        2. Seleciona Volume Mínimo: R$ 3.000.000
        3. Seleciona Margem EBIT Mínima: 0%
        4. Seleciona colunas (ROI, Margem EBIT, etc.)
        5. Clica em "Pesquisar"
        """
    
    def get_results_table(self) -> str:
        """Retorna HTML da tabela de resultados"""
```

**XPaths importantes:**
```python
# Elementos do formulário
VOLUME_INPUT_XPATH = "//input[@id='...']"
EBIT_DROPDOWN_XPATH = "//select[@name='...']"

# Tabela de resultados
RESULTS_TABLE_XPATH = "//table[@class='results']"
```

#### `outbound/database/excel_stock_repository.py`

```python
class ExcelStockRepository(StockRepositoryPort):
    """Adapter para salvar resultados em Excel"""
    
    def save(self, stocks: pd.DataFrame) -> None:
        """
        Salva ações em arquivo Excel
        
        Caminho: definido em constants.OUTPUT_FILE
        Planilha: constants.OUTPUT_SHEET
        """
```

---

### Diretório: `src/rank/application/`

**Responsabilidade**: Orquestração de casos de uso

#### `find_stoks_use_case.py`

```python
class FindStoksUseCase(FindStoksUseCasePort):
    """
    Caso de uso principal - coordena todo o fluxo
    
    Passos:
    1. Scraping de ações não-financeiras
    2. Scraping de ações financeiras
    3. Merge de DataFrames
    4. Cálculo de volatilidade
    5. Aplicação de filtros
    6. Enriquecimento com detalhes
    7. Salvamento em Excel
    """
    
    def execute(self):
        """Executa o fluxo completo"""
        # Scraping
        html_nf = self._perform_scraping(False)
        df_nf = self._extraction_service.extract_from_html(html_nf, False)
        
        html_fin = self._perform_scraping(True)
        df_fin = self._extraction_service.extract_from_html(html_fin, True)
        
        # Merge
        df_combined = pd.concat([df_nf, df_fin], ignore_index=True)
        
        # Processamento
        df_volatility = self._calculate_volatility(df_combined)
        df_filtered = self._apply_filters(df_volatility)
        df_enriched = self._enrich_with_details(df_filtered)
        
        # Salvamento
        self._save_results(df_enriched)
```

---

## Fluxo de Dados

```
┌──────────────────────────────────────────────────┐
│  main.py                                         │
│  ├─ Chama: initialize_di()                      │
│  └─ Executa: controller.start_scraping()        │
└──────────────┬───────────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────────┐
│  dependency_injection.py                         │
│  Cria instâncias e injeta dependências           │
└──────────────┬───────────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────────┐
│  StartScrapingController.start_scraping()        │
└──────────────┬───────────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────────┐
│  FindStoksUseCase.execute()                      │
├─ Chama: _perform_scraping(False) [não-fin]      │
│  └─ InvestSiteScrapingAdapter.apply_filters()   │
│  └─ InvestSiteScrapingAdapter.get_results_table()
├─ Chama: _perform_scraping(True) [fin]           │
│  └─ InvestSiteFinancialScrapingAdapter...       │
├─ Chama: StockExtractionService.extract_from_html()
├─ Chama: _calculate_volatility()                 │
│  └─ StockVolatilityService.calculate_volatility()
├─ Chama: _apply_filters()                        │
│  └─ StockFilterService.apply_all_filters()      │
├─ Chama: _enrich_with_details()                  │
│  └─ InvestSiteDetailsPageScrapingAdapter...     │
│  └─ Invest10DetailsPageScrapingAdapter...       │
└─ Chama: _save_results()                         │
   └─ ExcelStockRepository.save()                 │
```

---

## Como Adicionar Novos Componentes

### Adicionar Novo Filtro

**1. Adicionar método no `StockFilterService`:**

```python
class StockFilterService:
    # ... métodos existentes ...
    
    def _filter_by_dividend_yield(self, df: pd.DataFrame) -> pd.DataFrame:
        """Remove ações com DY menor que X%"""
        return df[df['DY'] > 2.0]  # Exemplo: DY mínimo 2%
```

**2. Chamar no método `apply_all_filters()`:**

```python
def apply_all_filters(self, df: pd.DataFrame) -> pd.DataFrame:
    df = self._remove_insurers(df)
    df = self._remove_bdrs(df)
    df = self._remove_duplicates(df)
    df = self._filter_by_dividend_yield(df)  # NOVO
    # ... resto dos filtros
    return df
```

### Adicionar Novo Adapter de Scraping

**1. Criar classe em `src/rank/adapters/outbound/scraping/`:**

```python
# novo_site_adapter.py

from src.rank.ports.outbound.Invest_site_scraping_port import InvestSiteScrapingPort

class NovoSiteScrapingAdapter(InvestSiteScrapingPort):
    """Adapter para novo site de scraping"""
    
    def __init__(self, web_driver: WebScrapingDriver):
        self.web_driver = web_driver
        self.url = "https://novo-site.com.br/acoes"
    
    def apply_filters(self):
        """Implementar aplicação de filtros específica"""
        pass
    
    def get_results_table(self) -> str:
        """Implementar extração de HTML"""
        pass
```

**2. Registrar em `dependency_injection.py`:**

```python
from src.rank.adapters.outbound.scraping.novo_site_adapter import NovoSiteScrapingAdapter

def initialize_di() -> tuple[StartScrapingController, WebScrapingDriver]:
    web_scraping = WebScrapingDriver()
    novo_adapter = NovoSiteScrapingAdapter(web_scraping)
    
    # ... resto da injeção ...
```

**3. Usar no caso de uso:**

```python
class FindStoksUseCase(FindStoksUseCasePort):
    def __init__(self, novo_adapter: NovoSiteScrapingAdapter, ...):
        self._novo_adapter = novo_adapter
    
    def execute(self):
        html = self._novo_adapter.apply_filters()
        # ... processar ...
```

### Adicionar Novo Repositório

**1. Criar classe em `src/rank/adapters/outbound/database/`:**

```python
# postgresql_stock_repository.py

from src.rank.ports.outbound.stock_repository_port import StockRepositoryPort

class PostgreSQLStockRepository(StockRepositoryPort):
    """Adapter para salvar em PostgreSQL"""
    
    def __init__(self, connection_string: str):
        self.engine = create_engine(connection_string)
    
    def save(self, stocks: pd.DataFrame) -> None:
        """Salva ações em banco PostgreSQL"""
        stocks.to_sql('stocks', self.engine, if_exists='replace')
```

**2. Atualizar `dependency_injection.py`:**

```python
def initialize_di() -> tuple[StartScrapingController, WebScrapingDriver]:
    # ... adapters existentes ...
    
    # Novo repositório
    repository = PostgreSQLStockRepository(POSTGRESQL_CVM_URL)
    
    # ... resto da injeção ...
```

---

## Testabilidade

### Criar Mocks para Testes

**Exemplo: Mock do WebScrapingDriver**

```python
from unittest.mock import Mock

class MockWebScrapingDriver:
    def navigate_to(self, url: str):
        pass
    
    def click_element(self, xpath: str):
        pass
    
    def get_element_html(self, xpath: str) -> str:
        return "<html>...</html>"
    
    def close(self):
        pass

# Usar em testes
mock_driver = MockWebScrapingDriver()
adapter = InvestSiteScrapingAdapter(mock_driver)
```

**Exemplo: Mock do Repositório**

```python
class MockStockRepository(StockRepositoryPort):
    def __init__(self):
        self.saved_data = None
    
    def save(self, stocks: pd.DataFrame) -> None:
        self.saved_data = stocks
    
    def get_saved_data(self) -> pd.DataFrame:
        return self.saved_data

# Usar em testes
mock_repo = MockStockRepository()
use_case = FindStoksUseCase(..., mock_repo, ...)
use_case.execute()
assert len(mock_repo.get_saved_data()) > 0
```

### Vantagens da Arquitetura para Testes

- ✅ Interfaces permitem criar mocks facilmente
- ✅ Serviços de domínio são testáveis sem dependências externas
- ✅ Casos de uso podem ser testados com mocks injetados
- ✅ Adapters podem ser testados isoladamente

---

## Troubleshooting

### Problema: Timeout no Selenium

**Causa:** Site levando muito tempo para renderizar resultados

**Solução:**
```python
# Em constants.py, aumentar timeout
WAIT_TIME_AFTER_FILTER = 45  # Aumentar de 35 para 45
```

### Problema: XPath não encontrado

**Causa:** Site foi atualizado e estrutura HTML mudou

**Solução:**
1. Abrir Firefox manualmente
2. Abrir DevTools (F12)
3. Inspecionar elemento
4. Copiar XPath correto
5. Atualizar em adapter

```python
# Exemplo: Atualizar XPath em InvestSiteScrapingAdapter
OLD_XPATH = "//input[@id='volume']"
NEW_XPATH = "//input[@name='volume_minimo']"
```

### Problema: Erro ao calcular volatilidade

**Causa:** Ticker inválido ou não encontrado no yfinance

**Solução:** Verificar lista de tickers extraídos
```python
# Adicionar logging em StockVolatilityService
print(f"Buscando volatilidade para: {ticker}")
```

### Problema: Arquivo Excel não é gerado

**Causa:** Caminho inválido ou arquivo aberto

**Solução:**
1. Verificar se caminho em `OUTPUT_FILE` está correto
2. Fechar arquivo Excel se estiver aberto
3. Verificar permissões de escrita na pasta

```python
# Em constants.py
OUTPUT_FILE = r'C:\Users\thale\OneDrive\Finanças\rancking_acoes_brasileiras.xlsx'
# Verificar se pasta existe: C:\Users\thale\OneDrive\Finanças\
```

---

## Recursos Adicionais

- **ARQUITETURA.md**: Diagrama visual da arquitetura
- **readme.md**: Documentação geral do projeto
- **Código comentado**: Cada componente tem comentários explicativos

## Contato e Suporte

Para dúvidas sobre arquitetura ou implementação, revisar:
1. Comentários no código
2. ARQUITETURA.md para fluxogramas
3. Este guia para patterns

