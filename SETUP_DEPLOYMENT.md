# Setup e Deployment - Selecionador de Ações

## 📋 Tabela de Conteúdo

1. [Instalação Local](#instalação-local)
2. [Configuração do Ambiente](#configuração-do-ambiente)
3. [Execução da Aplicação](#execução-da-aplicação)
4. [Docker (Opcional)](#docker-opcional)
5. [Configurações Avançadas](#configurações-avançadas)

---

## Instalação Local

### Pré-requisitos

- **Python 3.11+** ([Download](https://www.python.org/downloads/))
- **Firefox** (navegador web) ([Download](https://www.mozilla.org/en-US/firefox/new/))
- **Git** (para clonar repositório) ([Download](https://git-scm.com/))
- **pip** (gerenciador de pacotes Python) - vem com Python

### Passo 1: Clonar o Repositório

```powershell
# PowerShell (Windows)
git clone https://github.com/seu-usuario/selecionador-acoes.git
cd selecionador-acoes
```

### Passo 2: Criar Ambiente Virtual

```powershell
# PowerShell (Windows)
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Se receber erro de permissão, executar PowerShell como administrador:
```powershell
# Como administrador
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\.venv\Scripts\Activate.ps1
```

### Passo 3: Instalar Dependências

```powershell
# Dentro do ambiente virtual
pip install -r ./app/requirements.txt
```

**Dependências instaladas:**
- `selenium` - Web automation
- `pandas` - Processamento de dados
- `openpyxl` - Leitura/escrita Excel
- `yfinance` - Dados financeiros
- `pydantic` - Validação de dados
- `sqlalchemy` - ORM
- `requests` - HTTP requests
- `lxml` - Parsing HTML

### Passo 4: Verificar Instalação

```powershell
# Testar import das bibliotecas
python -c "import selenium, pandas, openpyxl, yfinance; print('✓ Tudo instalado com sucesso!')"
```

---

## Configuração do Ambiente

### Editar Arquivo de Configuração

Abrir `app/src/common/constants.py` e ajustar:

#### 1. Caminho do Arquivo de Saída

```python
# ANTES
OUTPUT_FILE = r'C:\Users\thale\OneDrive\Finanças\rancking_acoes_brasileiras.xlsx'

# DEPOIS (seu caminho)
OUTPUT_FILE = r'C:\Seu\Caminho\Aqui\rancking_acoes_brasileiras.xlsx'
```

**Importante:** Certifique-se de que a pasta existe!

#### 2. Tempo de Espera do Scraping

```python
# PADRÃO (recomendado)
WAIT_TIME_AFTER_FILTER = 35  # 35 segundos

# Se o site está lento, aumentar para
WAIT_TIME_AFTER_FILTER = 45  # 45 segundos
```

#### 3. Parâmetros de Filtro

```python
# Volume financeiro mínimo
VOLUME_MINIMO = '3000000'  # R$ 3.000.000

# Margem EBIT mínima
MARGEM_EBIT_MINIMO = '0'

# Quantidade de resultados por página
QUANTIDADE_POR_PAGINA = '-1'  # -1 = todas as ações
```

#### 4. Modo Headless (Opcional)

```python
# PADRÃO: True (não mostra navegador)
WEBDRIVER_HEADLESS = True

# Para DEBUG: False (mostra Firefox aberto)
WEBDRIVER_HEADLESS = False
```

#### 5. Configurações de Volatilidade

```python
# Período para calcular volatilidade
VOLATILITY_PERIOD = "1y"  # 1 ano (padrão)
# Alternativas: "3mo", "6mo", "2y", "5y"

# Quantidade de ações por requisição ao yfinance
VOLATILITY_BATCH_SIZE = 10  # Processar 10 ações por vez

# Delay entre requisições (em segundos)
VOLATILITY_DELAY_BETWEEN_BATCHES = 0.5  # Meio segundo
```

### (Opcional) Configurar PostgreSQL

Se quiser usar banco de dados em vez de Excel:

```python
# Connection string PostgreSQL
POSTGRESQL_CVM_URL = "postgresql://usuario:senha@localhost:5432/seu_banco"

# Exemplo com valores reais:
POSTGRESQL_CVM_URL = "postgresql://postgres:minhasenha@localhost:5432/acoes_db"
```

---

## Execução da Aplicação

### Execução Simples

```powershell
# Dentro do ambiente virtual
cd app
python main.py
```

### O que Acontece

1. 🔍 Scraping de ações não-financeiras (≈35 segundos)
2. 🔍 Scraping de ações financeiras (≈35 segundos)
3. 📊 Extração de dados (≈1 minuto)
4. 📈 Cálculo de volatilidade (≈5-10 minutos, depende do yfinance)
5. 🔎 Enriquecimento com detalhes (≈5-10 minutos)
6. 💾 Salvamento em Excel (≈10 segundos)

**Tempo total estimado: 15-30 minutos**

### Monitorar Execução

O programa exibe mensagens de progresso:

```
Aplicando filtros no site...
Total de ações após juntar financeiras e não-financeiras: 245
Aplicando filtros de negócio...
Total de ações após filtros: 187
Calculando volatilidade das ações...
Volatilidade adicionada ao resultado!
Capturando detalhes das ações...
Detalhes adicionados!
Salvando resultados em Excel...
✓ Ações salvas com sucesso em: C:\Seu\Caminho\rancking_acoes_brasileiras.xlsx
```

### Parar Execução

Pressionar `Ctrl + C` para interromper (fará cleanup automático).

---

## Docker (Opcional)

Para executar em container Docker (sem necessidade de instalar dependências localmente):

### Pré-requisitos

- Docker Desktop instalado ([Download](https://www.docker.com/products/docker-desktop))

### Build da Imagem

```powershell
# Na raiz do projeto
docker build -t selecionador-acoes:latest .
```

### Executar Container

```powershell
# Executar com saída interativa
docker run -it --rm -v C:\Seu\Caminho:/app/output selecionador-acoes:latest
```

### Com Docker Compose

```powershell
# Na raiz do projeto
docker-compose up
```

**Nota:** O arquivo de saída será criado em `/app/output` dentro do container.

---

## Configurações Avançadas

### Debug Mode

Para ver o Firefox em ação e debug:

```python
# Em app/src/common/constants.py
WEBDRIVER_HEADLESS = False
WAIT_TIME_AFTER_FILTER = 60  # Tempo maior para inspecionar
```

Depois executar:
```powershell
python main.py
```

Agora você pode ver o navegador fazendo o scraping e ter mais tempo para ver o que está acontecendo.

### Logging

Para adicionar logs mais detalhados:

```python
# Em app/main.py, adicionar no início:
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

### Customizar Saída Excel

Editar `app/src/rank/adapters/outbound/database/excel_stock_repository.py`:

```python
class ExcelStockRepository(StockRepositoryPort):
    def save(self, stocks: pd.DataFrame) -> None:
        # Customizar formatação
        with pd.ExcelWriter(OUTPUT_FILE, engine='openpyxl') as writer:
            stocks.to_excel(writer, sheet_name=OUTPUT_SHEET, index=False)
            
            # Exemplo: Auto-ajustar largura das colunas
            worksheet = writer.sheets[OUTPUT_SHEET]
            for idx, col in enumerate(stocks.columns):
                max_length = max(
                    stocks[col].astype(str).map(len).max(),
                    len(col)
                )
                worksheet.column_dimensions[chr(65 + idx)].width = max_length + 2
```

### Executar Periodicamente (Windows Task Scheduler)

Para executar automaticamente todos os dias:

1. Abrir **Task Scheduler** (Win + R → "taskschd.msc")
2. Criar **New Task**:
   - **Name:** Selecionador de Ações
   - **Trigger:** Daily at 22:00 (ou horário desejado)
   - **Action:** Start a program
     - **Program:** `C:\Users\seu_usuario\.venv\Scripts\python.exe`
     - **Arguments:** `C:\Seu\Caminho\selecionador-acoes\app\main.py`
     - **Start in:** `C:\Seu\Caminho\selecionador-acoes\app`

### Executar com Cron (Linux/Mac)

Se usar em Linux/Mac:

```bash
# Editar crontab
crontab -e

# Adicionar linha para executar todo dia às 22:00
0 22 * * * cd /seu/caminho/selecionador-acoes && ./.venv/bin/python app/main.py
```

---

## Troubleshooting

### Problema: "ModuleNotFoundError: No module named 'selenium'"

**Solução:**
```powershell
# Verificar se ambiente virtual está ativado
# Deve aparecer (.venv) no prompt

# Se não, ativar:
.\.venv\Scripts\Activate.ps1

# Instalar novamente:
pip install -r ./app/requirements.txt
```

### Problema: "geckodriver not found"

**Solução:**
```powershell
# GeckoDriver já está no projeto em selecionador-acoes/geckodriver.exe
# Se não estiver:

# 1. Download de https://github.com/mozilla/geckodriver/releases
# 2. Extrair geckodriver.exe
# 3. Colocar na raiz do projeto (C:\...\selecionador-acoes\)
```

### Problema: Firefox não abre

**Solução:**
```powershell
# Verificar se Firefox está instalado
firefox --version

# Se não estiver, baixar em https://www.mozilla.org
```

### Problema: "Connection timeout" ao scraping

**Solução:**
```python
# Aumentar tempo de espera em constants.py
WAIT_TIME_AFTER_FILTER = 60  # Aumentar mais

# Ou verificar:
# - Conexão de internet
# - Se o site investsite.com.br está online
# - Se não há firewall bloqueando
```

### Problema: "ModuleNotFoundError: No module named 'app'"

**Solução:**
```powershell
# Certifique-se de estar rodando de dentro de app/
cd app
python main.py

# OU executar do diretório raiz
python -m app.main
```

### Problema: Excel não é criado

**Solução:**
```python
# 1. Verificar se caminho está correto em constants.py:
OUTPUT_FILE = r'C:\Seu\Caminho\rancking_acoes_brasileiras.xlsx'

# 2. Verificar se pasta existe:
# C:\Seu\Caminho\ deve existir

# 3. Fechar Excel se arquivo estiver aberto

# 4. Verificar permissões de escrita:
# Clicar direito na pasta → Propriedades → Segurança
```

---

## Verificação de Saúde

Para verificar se tudo está funcionando:

```powershell
# 1. Python instalado?
python --version  # Deve ser 3.11+

# 2. Ambiente virtual criado?
.\.venv\Scripts\Activate.ps1

# 3. Dependências instaladas?
pip list | grep selenium
pip list | grep pandas

# 4. Firefox instalado?
firefox --version

# 5. GeckoDriver presente?
dir geckodriver.exe

# 6. Arquivo de configuração OK?
# Abrir app/src/common/constants.py e verificar paths
```

Se todos os itens acima estiverem OK, a aplicação deve funcionar!

---

## Próximos Passos

1. ✅ Verificar todos os pré-requisitos
2. ✅ Clonar repositório
3. ✅ Criar ambiente virtual
4. ✅ Instalar dependências
5. ✅ Editar `constants.py` com seus paths
6. ✅ Executar `python main.py`
7. ✅ Verificar arquivo Excel gerado

Sucesso! 🚀

