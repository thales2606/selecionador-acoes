# Selecionador de Ações - Arquitetura Hexagonal

Aplicação de seleção e filtragem automática de ações brasileiras com análise de volatilidade, utilizando web scraping, Arquitetura Hexagonal e Clean Code.

## 🎯 Objetivo

Identificar automaticamente ações brasileiras seguindo critérios técnicos de análise fundamental e volatilidade, diferenciando entre empresas financeiras e não-financeiras, gerando relatório em Excel para investimento.

## ⚙️ Setup Local

### Pré-requisitos
- Python 3.11+
- pip ou conda
- Firefox (para Selenium WebDriver)
- GeckoDriver (já incluído no projeto)

### Instalação

```bash
# Criar ambiente virtual
python -m venv .venv

# Ativar ambiente virtual (Windows)
.\.venv\Scripts\activate

# Instalar dependências
pip install -r ./app/requirements.txt
```

## 🏗️ Arquitetura

Este projeto segue os princípios da **Arquitetura Hexagonal (Ports & Adapters)**, **Clean Code** e **Domain-Driven Design**.

### Estrutura de Pastas

```
app/
├── src/
│   ├── common/              # Constantes e configurações compartilhadas
│   │   └── constants.py     # URLs, timeouts, paths
│   ├── domain/              # Lógica de negócio pura (independente de frameworks)
│   │   ├── services/        # Serviços de domínio
│   │   │   ├── stock_extraction_service.py
│   │   │   ├── stock_filter_service.py
│   │   │   └── stock_volatility_service.py
│   │   └── value_objects/   # Objetos de valor
│   └── rank/                # Módulo principal (casos de uso e adapters)
│       ├── adapters/        # Implementações de interfaces
│       │   ├── inbound/     # Controllers/entry points
│       │   │   └── start_scraping.py
│       │   └── outbound/    # Implementações de saída
│       │       ├── scraping/        # Web scraping
│       │       │   ├── web_scraping_driver.py
│       │       │   ├── invest_site_scraping_adapter.py
│       │       │   ├── invest_site_financial_scraping_adapter.py
│       │       │   ├── invest_site_details_page_scraping_adapter.py
│       │       │   └── invest_10_details_page_scraping_adapter.py
│       │       └── database/        # Persistência
│       │           └── excel_stock_repository.py
│       ├── application/     # Casos de uso
│       │   ├── find_stoks_use_case.py
│       │   └── dto/         # Data Transfer Objects
│       └── ports/           # Interfaces (contratos)
│           ├── inbound/
│           └── outbound/
├── dependency_injection.py  # Configuração de injeção de dependências
├── main.py                  # Ponto de entrada
└── requirements.txt         # Dependências
```

### Camadas Arquiteturais

#### 1. **Domain (Lógica de Negócio Pura)**

**Serviços:**
- `StockExtractionService`: Extrai dados de ações do HTML
- `StockFilterService`: Aplica regras de filtro (remove seguradoras, BDRs, duplicatas)
- `StockVolatilityService`: Calcula volatilidade anual via yfinance

### Ports (Interfaces)

**Inbound:**

#### 2. **Ports (Interfaces/Contratos)**

**Inbound:**
- `FindStoksUseCasePort`: Interface do caso de uso principal

**Outbound:**
- `InvestSiteScrapingPort`: Interface para web scraping de ações
- `DetailsPageScrapingPort`: Interface para scraping de detalhes de ações
- `StockRepositoryPort`: Interface para persistência de dados

#### 3. **Adapters (Implementações)**

**Inbound:**
- `StartScrapingController`: Entry point que orquestra o fluxo de scraping

**Outbound - Scraping:**
- `WebScrapingDriver`: Encapsula Selenium WebDriver (Firefox)
- `InvestSiteScrapingAdapter`: Scraping de ações não-financeiras
- `InvestSiteFinancialScrapingAdapter`: Scraping de ações financeiras
- `InvestSiteDetailsPageScrapingAdapter`: Detalhes de ações (InvestSite)
- `Invest10DetailsPageScrapingAdapter`: Detalhes de ações (Investidor10)

**Outbound - Persistência:**
- `ExcelStockRepository`: Salva resultados em arquivo Excel

#### 4. **Application (Casos de Uso)**

- `FindStoksUseCase`: Orquestra todo o fluxo:
  1. Realiza scraping de ações não-financeiras
  2. Realiza scraping de ações financeiras
  3. Combina resultados
  4. Calcula volatilidade
  5. Aplica filtros de negócio
  6. Enriquece com detalhes
  7. Salva em Excel

## 📊 Fluxo de Execução

```
┌─────────────────────────────────────────┐
│   StartScrapingController.start_scraping()
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  FindStoksUseCase.execute()              │
└──────────────┬──────────────────────────┘
               │
        ┌──────┴──────┐
        │             │
        ▼             ▼
  Scraping NF    Scraping FIN
  (35s wait)     (35s wait)
        │             │
        └──────┬──────┘
               ▼
     Merge DataFrames
               ▼
    Calcular Volatilidade
               ▼
     Aplicar Filtros
               ▼
   Enriquecer com Detalhes
               ▼
    Salvar em Excel
```

## 📋 Critérios de Seleção

### Filtros no Site InvestSite (Pré-Filtragem)

#### Ações Não-Financeiras
- **Volume Financeiro Mínimo:** R$ 3.000.000
- **Margem EBIT Mínima:** 0%
- **Colunas Selecionadas:** ROI, Margem EBIT, EV/EBIT, DY, Volume, Market Cap

#### Ações Financeiras
- **Volume Diário Médio Mínimo:** R$ 3.000.000 (últimos 3 meses)
- **Colunas Selecionadas:** ROE, Margem Líquida, Alavancagem, P/E, P/B, DY, Volume Diário, Market Cap

### Filtros na Aplicação (Pós-Filtragem)

1. **Remoção de Seguradoras**
   - Remove empresas do setor de seguros que distorcem análise fundamental

2. **Remoção de BDRs (Brazilian Depositary Receipts)**
   - Mantém apenas ações ordinárias (remove tickers com '33')

3. **Deduplicação por Volume**
   - Uma ação por empresa, mantendo a com maior volume financeiro

4. **Validação de Dados**
   - Remove registros com valores ausentes em colunas críticas

5. **Ranking por Valuation**
   - Ordena por EV/EBIT (múltiplo de valuation)

### Enriquecimento de Dados

- **Volatilidade Anual:** Calculada via yfinance (1 ano de dados)
- **Detalhes Técnicos:** Scraped de InvestSite e Investidor10
  - Dividend Yield atualizado
  - Últimas cotações
  - Outros indicadores técnicos

## 🚀 Como Usar

### Executar Aplicação

```bash
# Ativar ambiente virtual
.\.venv\Scripts\activate

# Executar
python app/main.py
```

### Customizar Execução

Editar `app/dependency_injection.py` e `app/src/common/constants.py` para:
- Mudar caminho do arquivo de saída (`OUTPUT_FILE`)
- Ajustar timeouts (`WAIT_TIME_AFTER_FILTER`)
- Modificar parâmetros de filtro (`VOLUME_MINIMO`, `MARGEM_EBIT_MINIMO`)
- Configurar headless mode (`WEBDRIVER_HEADLESS`)

### Exemplo de Uso Programático

```python
from app.dependency_injection import initialize_di

# Inicializar injeção de dependências
controller, web_scraping = initialize_di()

try:
    # Executar scraping e filtragem
    controller.start_scraping()
finally:
    # Liberar recursos
    web_scraping.close()
```

## 🔧 Tecnologias Utilizadas

| Tecnologia | Versão | Propósito |
|------------|--------|----------|
| Python | 3.11+ | Linguagem principal |
| Selenium | 4.x | Web scraping/automation |
| Firefox | Latest | Navegador para Selenium |
| Pandas | 2.x | Processamento de dados |
| OpenPyXL | 3.x | Escrita em Excel |
| yfinance | Latest | Dados financeiros |
| SQLAlchemy | 2.x | ORM (para futuro) |
| Pydantic | 2.x | Validação de dados |

## 📦 Dependências Principais

```
pydantic          # Validação e serialização de dados
selenium          # Web automation e scraping
yfinance          # Dados históricos de ações
pandas            # Processamento de dados tabulares
openpyxl          # Leitura/escrita de arquivos Excel
lxml              # Parsing de HTML/XML
sqlalchemy        # ORM e acesso a banco de dados
psycopg2-binary   # Driver PostgreSQL
requests          # Requisições HTTP
```

Veja `app/requirements.txt` para todas as dependências.

## 🧪 Padrões de Design Utilizados

- **Hexagonal Architecture**: Separação clara entre domínio, ports e adapters
- **Dependency Injection**: Facilita testes e manutenção
- **Strategy Pattern**: Diferentes adapters para diferentes fontes de dados
- **Template Method**: `FindStoksUseCase.execute()` define o fluxo padrão
- **Factory Pattern**: `initialize_di()` cria instâncias configuradas
- **Repository Pattern**: Abstração de persistência
- **Service Layer**: Serviços de domínio independentes

## ✨ Benefícios da Arquitetura

1. **Independência de Frameworks**: Lógica de negócio não depende de bibliotecas externas
2. **Testabilidade**: Interfaces permitem criar mocks facilmente
3. **Manutenibilidade**: Código bem organizado em camadas
4. **Escalabilidade**: Fácil adicionar novos adapters (novos sites, repositórios, etc.)
5. **Flexibilidade**: Trocar implementações sem afetar regra de negócio
6. **Reutilização**: Componentes podem ser reutilizados em diferentes contextos

## 🔌 Extensibilidade

### Adicionar Novo Site de Scraping

1. Criar novo adapter em `src/rank/adapters/outbound/scraping/`
2. Implementar `InvestSiteScrapingPort`
3. Registrar em `dependency_injection.py`

### Adicionar Novo Repositório

1. Criar adapter em `src/rank/adapters/outbound/database/`
2. Implementar `StockRepositoryPort`
3. Usar em `FindStoksUseCase`

### Adicionar Novo Serviço

1. Criar classe em `src/domain/services/`
2. Injetar em `FindStoksUseCase`
3. Chamar no método apropriado
