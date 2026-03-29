# Arquitetura da Solução - Financeiras vs Não-Financeiras

## Diagrama de Fluxo de Dependências

```
┌─────────────────────────────────────────────────────────────────┐
│                        DEPENDENCY INJECTION                     │
│            (app/dependency_injection.py - initialize_di)        │
└────────────────────────────┬────────────────────────────────────┘
                             │
                    ┌────────▼────────┐
                    │ financial=True? │
                    └────────┬────────┘
                    ┌────────┴────────┐
                    │                 │
            ┌───────▼─────────┐    ┌──▼──────────────┐
            │  financial=FALSE │    │  financial=TRUE │
            │  (ou padrão)     │    │                 │
            └────────┬────────┘    └────────┬────────┘
                     │                      │
        ┌────────────▼───────────┐ ┌────────▼──────────────┐
        │  URL_INVESTSITE        │ │ URL_INVESTSITE_FINAN │
        │  seleciona_acoes.php   │ │ seleciona_acoes_fin  │
        └────────────┬───────────┘ └────────┬──────────────┘
                     │                      │
        ┌────────────▼────────────────────┐ │
        │  WebScrapingDriver               │ │
        │  (Selenium Firefox)              │ │
        └────────────┬────────────────────┘ │
                     │                       │
        ┌────────────▼────────────────┐     │
        │  Adapter Selection          │     │
        └────────────┬────────────────┘     │
                     │                      │
        ┌────────────┴──────────────┐       │
        │                           │       │
┌───────▼─────────────────┐  ┌─────▼──────────────────────┐
│ InvestSiteScrapingAdapter│  │ InvestSiteFinancialScrapingAdapter
│                          │  │                           │
│ Filtros:                │  │ Filtros:                 │
│ - ROI                   │  │ - ROE (itm7)             │
│ - Margem EBIT           │  │ - Margem Líquida (itm9)  │
│ - EV/EBIT               │  │ - Alavancagem (itm12)    │
│ - DY                    │  │ - P/E (itm14)            │
│ - Volume Financeiro     │  │ - P/B (itm15)            │
│ - Market Cap            │  │ - DY (itm19)             │
│                          │  │ - Volume Diário (itm20)  │
│ XPaths: itm8,13,26,32... │  │ - Market Cap (itm21)     │
│                          │  │                           │
│ apply_filters()          │  │ XPaths: itm7,9,12,14,15  │
│ get_results_table()      │  │ apply_filters()           │
└───────┬──────────────────┘  │ get_results_table()       │
        │                     └─────┬──────────────────────┘
        │                           │
        └───────────────┬───────────┘
                        │
        ┌───────────────▼────────────────┐
        │  StockExtractionService        │
        │  (Extract from HTML)           │
        └───────────────┬────────────────┘
                        │
        ┌───────────────▼────────────────┐
        │  StockFilterService            │
        │  (Apply business rules)        │
        │  - Remove insurers             │
        │  - Remove BDRs                 │
        │  - Remove duplicates           │
        └───────────────┬────────────────┘
                        │
        ┌───────────────▼────────────────┐
        │  StockVolatilityService        │
        │  (Calculate 1-year volatility) │
        └───────────────┬────────────────┘
                        │
        ┌───────────────▼────────────────┐
        │  ExcelStockRepository          │
        │  (Save results)                │
        └────────────────────────────────┘
```

## Estrutura de Classes

```
┌─────────────────────────────────────────┐
│  PORT: InvestSiteScrapingPort (Abstract)│
│  ├─ apply_filters()                     │
│  └─ get_results_table()                 │
└────────────────────┬────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
┌───────▼──────────────────┐   ┌──▼──────────────────────────┐
│ InvestSiteScrapingAdapter │   │ InvestSiteFinancialAdapter │
│ (Ações Não-Financeiras)   │   │ (Ações Financeiras)        │
│ ├─ apply_filters()        │   │ ├─ apply_filters()         │
│ ├─ get_results_table()    │   │ ├─ get_results_table()     │
│ └─ _select_filter()       │   │ └─ _select_filter()        │
└──────────────────────────┘   └────────────────────────────┘
```

## Fluxo de Dados

### Cenário 1: Buscar Ações Não-Financeiras
```
initialize_di(financial=False)
    ↓
URL_INVESTSITE
    ↓
InvestSiteScrapingAdapter
    ↓
apply_filters() com ROI, Margem EBIT, EV/EBIT, ...
    ↓
get_results_table()
    ↓
Processar e salvar em Excel
```

### Cenário 2: Buscar Ações de Empresas Financeiras
```
initialize_di(financial=True)
    ↓
URL_INVESTSITE_FINANCEIRAS
    ↓
InvestSiteFinancialScrapingAdapter
    ↓
apply_filters() com ROE, Margem Líquida, Alavancagem, ...
    ↓
get_results_table()
    ↓
Processar e salvar em Excel
```

## Componentes Compartilhados

```
┌────────────────────────────────────────┐
│  WebScrapingDriver                     │
│  (Controla Selenium Firefox)           │
│  ├─ navigate_to()                      │
│  ├─ click_element()                    │
│  ├─ send_keys_to_element()             │
│  ├─ get_element_html()                 │
│  ├─ select_dropdown_value()            │
│  └─ close()                            │
└────────────────────────────────────────┘
                ↑
                │ Usado por
                │
    ┌───────────┴──────────────┐
    │                          │
InvestSiteScrapingAdapter    InvestSiteFinancialScrapingAdapter
```

## Ciclo de Vida da Aplicação

```
1. INICIALIZAÇÃO
   ↓
2. DECISÃO (Financial?)
   ├─ SIM → Use InvestSiteFinancialScrapingAdapter
   └─ NÃO → Use InvestSiteScrapingAdapter
   ↓
3. NAVEGAÇÃO
   └─ Vai para URL específica
   ↓
4. APLICAÇÃO DE FILTROS
   └─ Seleciona checkboxes e valores
   ↓
5. AGUARDAMENTO
   └─ Espera 35 segundos
   ↓
6. EXTRAÇÃO
   └─ Pega HTML da tabela
   ↓
7. PROCESSAMENTO
   ├─ Extrai dados
   ├─ Aplica filtros
   └─ Calcula volatilidade
   ↓
8. PERSISTÊNCIA
   └─ Salva em Excel
   ↓
9. LIMPEZA
   └─ Fecha WebDriver
```

## Matriz de Decisão

| Requisito | Não-Financeiras | Financeiras |
|-----------|-----------------|-------------|
| **URL** | seleciona_acoes.php | seleciona_acoes_financ.php |
| **Adapter** | InvestSiteScrapingAdapter | InvestSiteFinancialScrapingAdapter |
| **Parâmetro DI** | financial=False | financial=True |
| **Indicadores** | ROI, EBIT, EV/EBIT, DY, Vol, Cap | ROE, Mar.Liq, Alavancagem, P/E, P/B, DY, Vol, Cap |
| **Volume Mínimo** | R$ 3.000.000 (Vol.Fin.) | R$ 3.000.000 (Vol.Diário 3m) |
| **Filtros Pós** | Remove seguradoras, BDRs, duplicatas | Filtros gerais aplicáveis |

## Extensibilidade

```
Para adicionar novo tipo de ação:

1. Criar novo adapter:
   class InvestSite[Tipo]ScrapingAdapter(InvestSiteScrapingPort)

2. Adicionar constante em constants.py:
   URL_INVESTSITE_[TIPO] = "..."

3. Atualizar initialize_di():
   if financial_subtype == "meu_tipo":
       url = URL_INVESTSITE_MEU_TIPO
       invest_adapter = InvestSiteMeuTipoAdapter(web_scraping)

4. Pronto! Arquitetura permite fácil extensão.
```

## Padrões de Design Utilizados

- **Strategy Pattern**: Diferentes adapters para diferentes estratégias de scraping
- **Adapter Pattern**: Convertem XPath/Selenium em interface genérica
- **Dependency Injection**: Injeção de dependências via `initialize_di()`
- **Factory Pattern**: `initialize_di()` funciona como factory
- **Template Method**: `FindStoksUseCase.execute()` define template do fluxo

## Observações de Segurança

- XPaths são mantidos em constantes para fácil atualização
- WebDriver é fechado após uso (no `finally` do `execute()`)
- Tratamento de erro para dropdown com try/except
- Timeouts para evitar hangs infinitos

