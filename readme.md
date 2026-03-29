# Selecionador de Ações - Arquitetura Hexagonal

Aplicação de seleção e filtragem de ações brasileiras utilizando web scraping e clean code.

## setup local

```bash
   ./.venv/Scripts/pip3.13 install -r ./app/requirements.txt
```
   


## Arquitetura

Este projeto segue os princípios da **Arquitetura Hexagonal (Ports & Adapters)** e **Clean Code**.

```
projeto/
├── domain/              # Camada de Domínio (lógica de negócio pura)
│   ├── entities/        # Entidades do domínio
│   ├── services/        # Serviços de domínio (lógica de negócio)
│   └── value_objects/   # Objetos de valor (opcional)
├── ports/               # Interfaces (contratos)
│   ├── inbound/         # Interfaces para entrada (casos de uso)
│   └── outbound/        # Interfaces para saída (external services)
├── adapters/            # Implementações dos interfaces
│   ├── inbound/         # Adaptadores de entrada (controllers, CLI)
│   └── outbound/        # Adaptadores de saída (web drivers, repositories)
├── application/         # Camada de aplicação (casos de uso)
│   ├── use_cases/       # Casos de uso (orquestração)
│   └── dto/             # Data Transfer Objects
├── config.py            # Configurações da aplicação
└── main.py              # Ponto de entrada
```

## Componentes Principais

### Domain (Camada de Domínio)

**Entidades:**
- `Stock`: Entidade de ação com atributos principais

**Serviços:**
- `StockFilterService`: Lógica de filtros de ações
- `StockExtractionService`: Extração de dados de ações

### Ports (Interfaces)

**Inbound:**
- `FindStoksUseCasePort`: Interface para buscar stocks

**Outbound:**
- `WebScrapingPort`: Interface para web scraping
- `StockFilterPort`: Interface para filtros
- `StockRepositoryPort`: Interface para persistência

### Adapters (Implementações)

**Inbound:**
- `StartScrapingController`: Controlador CLI que orquestra todo o fluxo

**Outbound:**
- `WebScrapingDriver`: Driver do Selenium implementando WebScrapingPort
- `InvestSiteScrapingAdapter`: Adapter para scraping de ações não-financeiras
- `InvestSiteFinancialScrapingAdapter`: Adapter para scraping de ações financeiras
- `DataFrameStockFilterAdapter`: Adapter de filtros com pandas
- `ExcelStockRepository`: Adapter para salvar em Excel

### Application (Casos de Uso)

- `FindStoksUseCase`: Orquestra a busca e filtragem de ações

## Critérios de Seleção de Ativos

Os filtros são aplicados em duas etapas:

### Etapa 1: Filtros no Site InvestSite (Pré-Filtragem)

1. **Volume Financeiro Mínimo: R$ 3.000.000**
   - Reduz risco operacional
   - Garante liquidez adequada para execução de operações
   - Reduz custo de transação

2. **Margem EBIT Mínima: 0%**
   - Remove empresas com margem EBIT negativa
   - Prioriza empresas com operações rentáveis

3. **Colunas Selecionadas para Análise:**
   - ROI (Retorno sobre Investimento)
   - Margem EBIT
   - EV/EBIT (múltiplo de valuation)
   - Dividend Yield (DY)
   - Volume Financeiro
   - Market Cap (Capitalização de Mercado)

### Etapa 2: Filtros Aplicados no Processamento de Dados

1. **Remoção de Seguradoras**
   - Remove: SUL AMÉRICA, PORTO SEGURO
   - Evita distorções causadas por empresas do setor de seguros

2. **Remoção de BDRs (Brazilian Depositary Receipts)**
   - Remove ações que contenham '33' no ticker
   - Foca em ações ordinárias listadas na B3

3. **Deduplicação por Volume Financeiro**
   - Remove duplicatas mantendo apenas a ação com maior volume
   - Garante uma única entrada por empresa

4. **Remoção de Registros sem Margem EBIT**
   - Remove linhas com valores ausentes na coluna Margem EBIT
   - Garante dados completos para análise

5. **Ordenação e Ranking por EV/EBIT**
   - Ordena em ordem ascendente (ações mais baratas primeiro)
   - Cria ranking para facilitar análise de valuation

## Como Usar

### Instalação

```bash
pip install -r requirements.txt
```

### Executar

#### Buscar ações não-financeiras
```python
from dependency_injection import initialize_di

controller = initialize_di(financial=False)
controller.start_scraping()
```

#### Buscar ações de empresas financeiras
```python
from dependency_injection import initialize_di

controller = initialize_di(financial=True)
controller.start_scraping()
```

Ou diretamente no `main.py`:

```bash
python main.py
```

## Suporte a Ações Financeiras e Não-Financeiras

A aplicação agora suporta a busca de dois tipos de ações:

### Ações Não-Financeiras
- **URL**: `https://www.investsite.com.br/seleciona_acoes.php`
- **Adapter**: `InvestSiteScrapingAdapter`
- **Uso**: `initialize_di(financial=False)` ou `initialize_di()`

Filtros aplicados:
- Volume Financeiro Mínimo: R$ 3.000.000
- Margem EBIT Mínima: 0%
- Colunas: ROI, Margem EBIT, EV/EBIT, DY, Volume e Market Cap

### Ações de Empresas Financeiras
- **URL**: `https://www.investsite.com.br/seleciona_acoes_financ.php`
- **Adapter**: `InvestSiteFinancialScrapingAdapter`
- **Uso**: `initialize_di(financial=True)`

Filtros aplicados para ações financeiras:
- Volume Diário Médio Mínimo: R$ 3.000.000 (últimos 3 meses)
- Colunas: ROE, Margem Líquida, Alavancagem, P/E, P/B, DY, Volume Diário e Market Cap



1. **Independência de Frameworks**: A lógica de negócio não depende de bibliotecas externas
2. **Testabilidade**: Interfaces permitem fácil criação de mocks
3. **Manutenibilidade**: Código organizado em camadas bem definidas
4. **Escalabilidade**: Fácil adicionar novos adaptadores
5. **Flexibilidade**: Trocar implementações sem afetale regra de negócio

## Exemplos de Extensão

### Adicionar novo repositório (ex: Banco de Dados)

1. Criar adapter em `adapters/outbound/database/db_stock_repository.py`
2. Implementar `StockRepositoryPort`
3. Atualizar `StartScrapingController`

### Adicionar novo seletor de site

1. Criar adapter em `adapters/outbound/scraping/novo_site_adapter.py`
2. Implementar a interface necessária
3. Usá-lo no controlador inbound

## Padrões de Design Utilizados

- **Strategy**: Diferentes filtros via `StockFilterService`
- **Adapter**: Conversão de interfaces externas
- **Dependency Injection**: Injeção de dependências
- **Repository**: Abstração de persistência
- **Service Layer**: Serviços de domínio
