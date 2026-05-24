
# URLs do site de scraping
URL_INVESTSITE = "https://www.investsite.com.br/seleciona_acoes.php"
URL_INVESTSITE_FINANCEIRAS = "https://www.investsite.com.br/seleciona_acoes_financ.php"
URL_INVESTSITE_DETAILS = "https://www.investsite.com.br/principais_indicadores.php?cod_negociacao="
URL_INVEST10_DETAILS = "https://investidor10.com.br/acoes/"

# Caminho do arquivo de saída
OUTPUT_FILE = r'C:\Users\thale\OneDrive\Finanças\rancking_acoes_brasileiras.xlsx'
OUTPUT_SHEET = 'Rancking de açoes Brasileiras'

# Parâmetros de scraping
WAIT_TIME_AFTER_FILTER = 35
VOLUME_MINIMO = '3000000'
MARGEM_EBIT_MINIMO = '0'
QUANTIDADE_POR_PAGINA = '-1'  # Todas as ações

# Configurações do webdriver
WEBDRIVER_HEADLESS = True

# Configurações PostgreSQL - CVM
# Formato: postgresql://user:password@host:port/database
# Exemplo: postgresql://cvm_user:cvm_password@localhost:5432/cvm_database
POSTGRESQL_CVM_URL = "postgresql://cvm_user:cvm_password@localhost:5432/cvm_database"

# URLs da CVM
CVM_BASE_URL = "http://dados.cvm.gov.br/dados/CIA_ABERTA"
CVM_COMPANIES_LIST_URL = "http://dados.cvm.gov.br/dados/CIA_ABERTA/CAD/DADOS/cad_cia_aberta.csv"

# Configurações de importação CVM
CVM_IMPORT_START_YEAR = 2017
CVM_BATCH_SIZE_COMPANIES = 100
CVM_BATCH_SIZE_FINANCIAL = 50

# Configurações de volatilidade
VOLATILITY_PERIOD = "1y"  # Período para calcular volatilidade
VOLATILITY_BATCH_SIZE = 10  # Quantidade de ações por requisição ao yfinance
VOLATILITY_DELAY_BETWEEN_BATCHES = 0.5  # Delay em segundos entre requisições

