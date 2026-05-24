# Plan: Implementar Requisitos de Ranqueamento de Ações

## TL;DR

Estender a aplicação com 3 novos filtros (volatilidade extrema, lucro líquido negativo, recuperação judicial) e 3 novos indicadores de ranking (Book to Market, Cash Flow Yield via EV/FCO, Earning Yield). Será necessário adicionar métodos em `StockFilterService`, criar novo `StockRankingService`, reordenar o fluxo em `FindStoksUseCase` para filtrar **após** enriquecimento, e adicionar tratamento robusto de conversão numérica.

---

## Requisitos Funcionais

### 1. Filtros de Exclusão

#### 1.1 Remover 10% das empresas com maior volatilidade
- **O quê**: Identificar top 10% por volatilidade e remover
- **Onde**: `StockFilterService._remove_top_10_percent_volatility()`
- **Entrada**: DataFrame com coluna `Volatilidade Anual (%)`
- **Saída**: DataFrame sem as 10% mais voláteis
- **Cálculo**: `quantile(0.9)` e filtrar `df[df['Volatilidade Anual (%)'] <= quantile]`

#### 1.2 Remover empresas com lucro líquido negativo
- **O quê**: Excluir empresas com lucro líquido negativo em 3 meses OU 1 ano
- **Onde**: `StockFilterService._remove_negative_net_profit()`
- **Entrada**: DataFrame com colunas `lucro_liquido_anual` e `lucro_liquido_trimestral`
- **Saída**: DataFrame sem lucros negativos
- **Lógica**: Se `lucro_liquido_anual < 0` OU `lucro_liquido_trimestral < 0` → remover
- **Detalhe**: Converter strings (formato "1.234.567,89") para float antes de comparar

#### 1.3 Remover empresas em recuperação judicial
- **O quê**: Excluir empresas com situação "Recuperação Judicial"
- **Onde**: `StockFilterService._remove_judicial_recovery()`
- **Entrada**: DataFrame com coluna `situacao_empresa` (vem de `InvestSiteDetailsPageScrapingAdapter`)
- **Saída**: DataFrame sem recuperação judicial
- **Lógica**: `df[~df['situacao_empresa'].str.contains('Recuperação Judicial', case=False, na=False)]`

### 2. Indicadores de Ranking

#### 2.1 Book to Market (Financeiras e Não-Financeiras)
- **Fórmula**: `Patrimônio Líquido / Market Cap`
- **Interpretação**: Maior é melhor (ação subavaliada)
- **Aplicável a**: Ambas financeiras e não-financeiras
- **Dados necessários**: `patrimonio_liquido` (Invest10), `Market Cap (R$)` (extraído)

#### 2.2 Cash Flow Yield (Somente Não-Financeiras)
- **Fórmula**: `1 / (EV/FCO)` ou equivalentemente `FCO / EV`
- **Interpretação**: Maior é melhor
- **Disponível**: `EV/FCO` já extraído do site
- **Para financeiras**: Deixar em branco (coluna vazia)
- **Detalhe**: `EV/FCO` é inverso (menor melhor), então usamos direto ou invertemos conforme necessário

#### 2.3 Earning Yield Operacional
- **Para não-financeiras**: `EBIT / EV` (já existe no site como `EV/EBIT`, inverso)
- **Para financeiras**: `Lucro Antes do Imposto de Renda / Market Cap`
- **Interpretação**: Maior é melhor
- **Dados necessários**: 
  - Não-financeiras: `EV/EBIT` (extraído do site) → usar `1 / EV/EBIT` ou deixar como está (menor melhor)
  - Financeiras: `imposto_anual` (Invest10) para calcular Lucro Antes IR = Lucro Líquido + Imposto

### 3. Dados a Obter nas Páginas de Detalhes

#### 3.1 De `InvestSiteDetailsPageScrapingAdapter`
- ✅ `situacao_empresa` - Já implementado (LABEL_SITUACAO_EMPRESA)

#### 3.2 De `Invest10DetailsPageScrapingAdapter`
- ✅ `lucro_liquido_anual` - Já implementado (_get_lucro_liquido(yearly=True))
- ✅ `lucro_liquido_trimestral` - Já implementado (_get_lucro_liquido(yearly=False))
- ✅ `patrimonio_liquido` - Já implementado (_get_patrimonio_liquido())
- ✅ `imposto_anual` - Já implementado (_get_tax())
- ✅ `imposto_trimestral` - Já implementado (_get_tax())

#### 3.3 Dados já na tabela extraída
- ✅ `EV/EBIT` - Coluna extraída (não-financeiras)
- ✅ `EV/FCO` - Coluna extraída (não-financeiras)
- ✅ `Market Cap (R$)` - Coluna extraída (ambas)
- ✅ `Volatilidade Anual (%)` - Calculada pelo `StockVolatilityService`

---

## Steps de Implementação

### Step 1: Criar utilitário de conversão numérica

**Arquivo**: `app/src/common/value_converters.py`

**Responsabilidades**:
- Converter string de valor monetário brasileiro para float
- Tratar formatos: "1.234.567,89", "1234567,89", "-1.234,56"
- Tratar valores nulos/vazios/None
- Retornar float ou None em caso de falha

**Função**: `convert_string_to_float(value: str | float | None) -> float | None`

**Exemplo**:
```python
convert_string_to_float("1.234.567,89") → 1234567.89
convert_string_to_float("-123,45") → -123.45
convert_string_to_float("") → None
convert_string_to_float(None) → None
```

---

### Step 2: Estender `StockFilterService`

**Arquivo**: `app/src/domain/services/stock_filter_service.py`

**Alterações**:
1. Adicionar import: `from src.common.value_converters import convert_string_to_float`
2. Adicionar novo método `_remove_top_10_percent_volatility()`
3. Adicionar novo método `_remove_negative_net_profit()`
4. Adicionar novo método `_remove_judicial_recovery()`
5. Atualizar `apply_all_filters()` para chamar os novos métodos na ordem correta

**Ordem de execução** no `apply_all_filters()`:
```python
df = self._remove_bdrs(df)                              # Já existe
df = self._remove_duplicates_keeping_highest_volume(df) # Já existe
df = self._remove_empty_ebit_margin(df)                 # Já existe
df = self._remove_judicial_recovery(df)                 # NOVO
df = self._remove_negative_net_profit(df)               # NOVO
df = self._remove_top_10_percent_volatility(df)         # NOVO
return df
```

---

### Step 3: Criar `StockRankingService`

**Arquivo**: `app/src/domain/services/stock_ranking_service.py`

**Responsabilidades**:
- Calcular indicadores de ranking para cada ação
- Adicionar colunas ao DataFrame com os indicadores calculados
- Lidar com conversões numéricas robustas
- Diferenciar entre financeiras e não-financeiras

**Métodos públicos**:
- `calculate_ranking_indicators(df: pd.DataFrame) -> pd.DataFrame` - Método principal

**Métodos privados**:
- `_calculate_book_to_market()` - Retorna Serie com os valores
- `_calculate_cash_flow_yield()` - Retorna Serie com os valores (None para financeiras)
- `_calculate_earning_yield()` - Retorna Serie com os valores (diferente por tipo)
- `_convert_and_get_float()` - Helper para converter valores da tabela

**Detalhes de implementação**:
- Book to Market: `patrimonio_liquido / Market Cap (R$)` para ambas
- Cash Flow Yield: `1 / EV/FCO` (ou usar EV/FCO direto) para não-financeiras, NaN para financeiras
- Earning Yield: `EBIT / EV` (usar `1 / EV/EBIT`) para não-fin; `(lucro_liquido_anual + imposto_anual) / Market Cap` para fin
- Adicionar colunas: `Book to Market`, `Cash Flow Yield`, `Earning Yield`

---

### Step 4: Reordenar fluxo em `FindStoksUseCase`

**Arquivo**: `app/src/rank/application/find_stoks_use_case.py`

**Alterações no `execute()`**:

**Ordem atual (incorreta)**:
```
1. Scraping
2. Extração
3. Volatilidade
4. Filtros          ← Problema: usa dados que ainda não foram enriquecidos
5. Enriquecimento
6. Salvar
```

**Ordem desejada (correta)**:
```
1. Scraping
2. Extração
3. Volatilidade
4. Enriquecimento   ← MOVIDO PARA ANTES dos filtros
5. Filtros         ← Agora tem todos os dados necessários
6. Ranking
7. Salvar
```

**Mudanças específicas**:
- Mover chamada de `_enrich_with_details()` para **antes** de `_apply_filters()`
- Adicionar nova chamada: `_apply_ranking()` após `_apply_filters()`
- Atualizar método `__init__()` para injetar `StockRankingService`

---

### Step 5: Adicionar `_apply_ranking()` em `FindStoksUseCase`

**Método novo**:
```python
def _apply_ranking(self, df: pd.DataFrame) -> pd.DataFrame:
    """Calcula indicadores de ranking"""
    print("Calculando indicadores de ranking...")
    df_ranked = self._ranking_service.calculate_ranking_indicators(df)
    print("Indicadores de ranking calculados com sucesso!")
    return df_ranked
```

---

### Step 6: Atualizar Injeção de Dependência

**Arquivo**: `app/dependency_injection.py`

**Alterações**:
1. Importar `StockRankingService`
2. Instanciar `StockRankingService` (sem dependências no construtor)
3. Injetar em `FindStoksUseCase.__init__()`
4. Garantir que é passado na inicialização do caso de uso

---

### Step 7: Atualizar `StockExtractionService`

**Arquivo**: `app/src/domain/services/stock_extraction_service.py`

**Verificações** (não há mudanças necessárias):
- ✅ Colunas já incluem: `EV/EBIT`, `EV/FCO`, `Market Cap (R$)`
- ✅ Coluna `Financeira` já é adicionada (diferencia tipos)
- ✅ Não é necessário adicionar colunas de indicadores aqui (será feito em `StockRankingService`)

---

## Fluxo Completo Atualizado

```
START
  ↓
Scraping (InvestSite)
  ├─ Ações não-financeiras
  └─ Ações financeiras (35-45 segundos)
  ↓
Extração de Dados (HTML → DataFrame)
  ├─ Colunas: Ação, Empresa, Preço, Margem EBIT, EV/EBIT, EV/FCO, Market Cap, ...
  └─ Coluna Financeira: 'Sim'/'Não'
  ↓
Cálculo de Volatilidade (yfinance)
  └─ Adiciona: Volatilidade Anual (%) (5-10 minutos)
  ↓
ENRIQUECIMENTO COM DETALHES ← MOVIDO PARA AQUI
  ├─ InvestSite: situacao_empresa
  └─ Invest10: lucro_liquido_anual, lucro_liquido_trimestral, patrimonio_liquido, imposto_anual
  ↓
FILTROS DE NEGÓCIO ← AGORA TEM TODOS OS DADOS
  ├─ Remove BDRs
  ├─ Remove duplicatas
  ├─ Remove margem EBIT vazia
  ├─ Remove Recuperação Judicial ← NOVO
  ├─ Remove Lucro Líquido Negativo ← NOVO
  └─ Remove Top 10% Volatilidade ← NOVO
  ↓
CÁLCULO DE INDICADORES DE RANKING ← NOVO
  ├─ Book to Market (ambas)
  ├─ Cash Flow Yield (não-fin apenas)
  └─ Earning Yield (diferente por tipo)
  ↓
Salvar em Excel
  └─ Arquivo com todas as colunas + indicadores + detalhes
END
```

---

## Considerações Técnicas

### 1. Tratamento de Valores Nulos

**Quando lucro líquido está vazio?**
- Considerar como "negativo" (remove a empresa)
- Motivo: Se não temos dados, não podemos validar se está saudável

**Implementação**:
```python
# Se valor está vazio/None → converter para float retorna None
# Depois: None < 0 → False, mas pd.isna(None) → True
# Solução: tratar None como negativo ou usar fillna(-1)
```

### 2. Ordem de Importância (Sugestão de Ranking)

**Prioridade para ordenação final**:
1. **EV/EBIT** (menor melhor) - Multiplicador de lucro
2. **Book to Market** (maior melhor) - Relação patrimônio/valor mercado
3. **Earning Yield** (maior melhor) - Rentabilidade operacional

### 3. Conversão de Valores

**Exemplos de formatos encontrados**:
- "1.234.567,89" → 1234567.89 (formato brasileiro com ponto milhar)
- "1234567,89" → 1234567.89 (sem separador milhar)
- "-123,45" → -123.45 (negativo)
- "" → None (vazio)
- None → None (nulo)

**Estratégia**: Função `convert_string_to_float()` que:
1. Recebe string, float ou None
2. Se já é float → retorna
3. Se é None/vazio → retorna None
4. Se é string → remove pontos, troca vírgula por ponto, converte
5. Em caso de erro → log + retorna None

### 4. Performance

**Impacto esperado**:
- Scraping: ~40 segundos (sem mudança)
- Volatilidade: ~5-10 minutos (sem mudança)
- Enriquecimento: ~5-10 minutos (REORDENADO - antes era depois dos filtros)
- Filtros: <1 segundo (operações em memória)
- Ranking: <1 segundo (cálculos simples)
- **Total estimado**: ~15-25 minutos (sem mudança significativa)

### 5. Dados Faltantes

**Problema**: Nem todas as ações têm todos os dados

**Solução por indicador**:
- **Book to Market**: Se patrimonio_liquido ou Market Cap ausentes → NaN
- **Cash Flow Yield**: Se EV/FCO ausente ou é financeira → NaN
- **Earning Yield**: Se EBIT/EV ausente ou dados inconsistentes → NaN

**Tratamento no Excel**: Usuário vê células vazias (NaN) para indicadores inaplicáveis

---

## Sequência de Commits Sugerida

1. `feat: adicionar value_converters.py para conversão numérica`
2. `feat: implementar StockRankingService com indicadores`
3. `refactor: reordenar fluxo em FindStoksUseCase (enriquecimento antes de filtros)`
4. `feat: adicionar filtros de volatilidade, lucro negativo e recuperação judicial`
5. `refactor: integrar StockRankingService via injeção de dependência`
6. `docs: atualizar README e ARQUITETURA.md com novos fluxo`

---

## Testes Sugeridos

### Unit Tests
- `test_convert_string_to_float()` - Todos os formatos
- `test_remove_top_10_percent_volatility()` - Com dados mock
- `test_remove_negative_net_profit()` - Com valores negativo/positivo/nulo
- `test_remove_judicial_recovery()` - Com diferentes situações
- `test_calculate_book_to_market()` - Cálculo correto
- `test_calculate_cash_flow_yield()` - Apenas não-financeiras, NaN para financeiras
- `test_calculate_earning_yield()` - Diferente por tipo

### Integration Tests
- Executar `execute()` com dataset pequeno
- Validar que resultado tem todas as colunas esperadas
- Validar que Excel gerado contém todos os indicadores

---

## Riscos e Mitigações

| Risco | Mitigação |
|-------|-----------|
| Perda de dados ao mover enriquecimento | Testes de integração verificam que cada row preserva dados |
| Valores nulos/ausentes quebram cálculos | Usar `pd.isna()`, `fillna()`, converter com tratamento de erro |
| Performance de enriquecimento aumenta | Aceitável segundo requisito (reordenar não aumenta tempo total) |
| Indicadores dão resultados inesperados | Validar com dados reais antes de mergear |
| Conversão numérica falha silenciosamente | Adicionar logs de erro em `value_converters.py` |

---

## Documentação a Atualizar

1. **README.md**
   - Adicionar novos filtros à seção "Critérios de Seleção"
   - Adicionar novos indicadores à seção "Indicadores Calculados"

2. **ARQUITETURA.md**
   - Atualizar diagrama de fluxo com novo `StockRankingService`
   - Atualizar matriz de decisão (se aplicável)
   - Adicionar seção sobre cálculo de indicadores

3. **GUIA_DESENVOLVIMENTO.md**
   - Adicionar exemplo: "Como adicionar um novo indicador"
   - Adicionar seção sobre conversão de valores

4. **EXEMPLOS_USO.md**
   - Adicionar exemplo de teste para `StockRankingService`
   - Adicionar snippet para usar `convert_string_to_float()`

---

## Checklist de Conclusão

- [ ] `value_converters.py` criado e testado
- [ ] `StockRankingService` implementado e testado
- [ ] `StockFilterService` estendido com 3 novos filtros
- [ ] `FindStoksUseCase` reordenado (enriquecimento antes de filtros)
- [ ] `FindStoksUseCase` inclui `_apply_ranking()`
- [ ] `dependency_injection.py` atualizado com novo serviço
- [ ] Testes unitários passando
- [ ] Teste de integração (execute completo) passando
- [ ] Excel gerado contém todas as colunas esperadas
- [ ] Documentação atualizada
- [ ] Commits bem organizados e comentados

---

## Notas Finais

1. **Reordenação de fluxo é crítica**: Os filtros de lucro líquido e recuperação judicial dependem dos dados enriquecidos. Mover enriquecimento para antes dos filtros é necessário.

2. **Conversão de valores é essencial**: Lucro líquido vem como string. Precisa converter para float antes de comparar com zero.

3. **EV/FCO vs FCO/EV**: Confirmado que usaremos EV/FCO (já existe) e deixaremos em branco para financeiras. Para o cálculo de Cash Flow Yield, podemos deixar como está ou inverter conforme necessário.

4. **Performance aceitável**: Reordenar não aumenta tempo total de execução significativamente, pois enriquecimento é operação sequencial (não paralelizável).

5. **Flexibilidade para futuro**: Novo `StockRankingService` permite adicionar mais indicadores facilmente no futuro.

