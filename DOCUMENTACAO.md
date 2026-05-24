# 📚 Documentação - Selecionador de Ações

Bem-vindo à documentação completa do **Selecionador de Ações**! 

Este projeto implementa uma arquitetura hexagonal robusta para scraping, filtragem e análise de ações brasileiras.

---

## 🗂️ Índice de Documentação

### 1. **[README.md](readme.md)** ← COMECE AQUI
   - 🎯 Objetivo do projeto
   - ⚙️ Setup local (instalação passo a passo)
   - 🏗️ Visão geral da arquitetura
   - 📊 Critérios de seleção de ações
   - 🚀 Como executar
   - 🔌 Extensibilidade

### 2. **[ARQUITETURA.md](ARQUITETURA.md)**
   - 📐 Diagrama de fluxo de dependências (visual)
   - 🔗 Estrutura de classes
   - 📉 Fluxo de dados detalhado
   - 🔀 Matriz de decisão (financeiras vs não-financeiras)
   - 🔧 Padrões de design utilizados
   - 🛡️ Observações de segurança

### 3. **[SETUP_DEPLOYMENT.md](SETUP_DEPLOYMENT.md)**
   - 📋 Instalação passo a passo (detalhada)
   - ⚙️ Configuração do ambiente
   - 🚀 Execução da aplicação
   - 🐳 Docker (opcional)
   - 🔧 Configurações avançadas
   - 🆘 Troubleshooting completo

### 4. **[GUIA_DESENVOLVIMENTO.md](GUIA_DESENVOLVIMENTO.md)**
   - 📖 Estrutura do projeto (linha por linha)
   - 🔄 Fluxo de dados (como tudo se conecta)
   - ➕ Como adicionar novos componentes
   - 🧪 Testabilidade e mocks
   - 🆘 Troubleshooting técnico

### 5. **[EXEMPLOS_USO.md](EXEMPLOS_USO.md)**
   - 💻 10 exemplos de código prontos para usar
   - 📝 Snippets para casos comuns
   - 🎯 Quick reference table
   - 💡 Dicas práticas

---

## 🚀 Quick Start (5 minutos)

### 1️⃣ Instalar Python 3.11+
```bash
# Verificar versão
python --version  # Deve ser 3.11+
```

### 2️⃣ Clonar Repositório
```bash
git clone https://seu-repo/selecionador-acoes.git
cd selecionador-acoes
```

### 3️⃣ Setup do Ambiente
```powershell
# Criar ambiente virtual
python -m venv .venv

# Ativar (Windows)
.\.venv\Scripts\Activate.ps1

# Instalar dependências
pip install -r ./app/requirements.txt
```

### 4️⃣ Configurar
Editar `app/src/common/constants.py`:
```python
OUTPUT_FILE = r'C:\Seu\Caminho\Aqui\rancking_acoes_brasileiras.xlsx'
```

### 5️⃣ Executar
```powershell
python app/main.py
```

**Pronto!** ✅ Arquivo Excel será gerado em ~15-30 minutos.

---

## 📋 Roteiros por Perfil

### 👤 Para Usuários Finais

1. Ler: **README.md** (seção "Como Usar")
2. Ler: **SETUP_DEPLOYMENT.md** (seção "Instalação Local")
3. Executar: `python app/main.py`
4. Consultar: **SETUP_DEPLOYMENT.md** (seção "Troubleshooting" se tiver problemas)

---

### 👨‍💻 Para Desenvolvedores

1. Ler: **README.md** (completo)
2. Ler: **ARQUITETURA.md** (para entender o design)
3. Ler: **GUIA_DESENVOLVIMENTO.md** (para detalhes técnicos)
4. Explorar: **EXEMPLOS_USO.md** (para começar a codificar)
5. Estudar: Código-fonte em `app/src/`

---

### 🏗️ Para Arquitetos de Software

1. Ler: **ARQUITETURA.md** (visão geral)
2. Ler: **GUIA_DESENVOLVIMENTO.md** (implementação)
3. Revisar: Arquivos em `app/src/rank/ports/` (interfaces)
4. Revisar: Arquivos em `app/src/domain/` (domínio puro)

---

### 🔧 Para DevOps/Infraestrutura

1. Ler: **SETUP_DEPLOYMENT.md** (seção "Docker")
2. Ler: **SETUP_DEPLOYMENT.md** (seção "Task Scheduler")
3. Revisar: `docker-compose.yml`
4. Revisar: `Dockerfile`

---

## 🎯 Encontrar Resposta Rápida

### "Como instalar?"
→ **SETUP_DEPLOYMENT.md** - Seção "Instalação Local"

### "Como executar?"
→ **README.md** - Seção "Como Usar"

### "O que é cada pasta?"
→ **GUIA_DESENVOLVIMENTO.md** - Seção "Estrutura do Projeto"

### "Quero adicionar um novo filtro"
→ **GUIA_DESENVOLVIMENTO.md** - Seção "Como Adicionar Novos Componentes"

### "Como testar meu código?"
→ **GUIA_DESENVOLVIMENTO.md** - Seção "Testabilidade"

### "Algo deu erro!"
→ **SETUP_DEPLOYMENT.md** - Seção "Troubleshooting"

### "Quero um exemplo de código"
→ **EXEMPLOS_USO.md** - 10 exemplos prontos

### "Como funciona a arquitetura?"
→ **ARQUITETURA.md** - Diagramas e fluxos

---

## 🗂️ Estrutura de Pastas

```
selecionador-acoes/
├── 📄 readme.md                    # ← COMECE AQUI
├── 📄 ARQUITETURA.md               # Diagramas e design
├── 📄 SETUP_DEPLOYMENT.md          # Setup e troubleshooting
├── 📄 GUIA_DESENVOLVIMENTO.md       # Guia técnico
├── 📄 EXEMPLOS_USO.md              # Exemplos de código
├── 📄 DOCUMENTACAO.md              # Este arquivo
│
├── app/
│   ├── main.py                     # Ponto de entrada
│   ├── dependency_injection.py     # Configuração de DI
│   ├── requirements.txt            # Dependências
│   │
│   └── src/
│       ├── common/
│       │   └── constants.py        # Configurações centralizadas
│       ├── domain/                 # Lógica de negócio pura
│       │   └── services/           # Serviços de domínio
│       └── rank/
│           ├── adapters/           # Implementações concretas
│           │   ├── inbound/        # Controllers
│           │   └── outbound/       # Drivers, repositórios, adapters
│           ├── application/        # Casos de uso
│           ├── ports/              # Interfaces/contratos
│           └── application/        # DTOs
│
├── docker-compose.yml              # Configuração Docker
├── Dockerfile                      # Build Docker
│
└── tests/                          # Testes unitários
    ├── test_cvm_module.py
    └── ...
```

---

## 🔑 Conceitos Principais

### Arquitetura Hexagonal
Separação clara entre:
- **Domain**: Lógica pura, independente de frameworks
- **Ports**: Contratos/interfaces
- **Adapters**: Implementações concretas

**Benefício**: Trocar componentes sem afetar lógica de negócio

### Injeção de Dependências
Todas as dependências são injetadas via `initialize_di()`

**Benefício**: Fácil criar mocks para testes

### Two-Pass Filtering
1. **Pré-filtragem no site**: Reduz volume de dados
2. **Pós-filtragem na aplicação**: Aplica regras de negócio

**Benefício**: Performance + flexibilidade

---

## 📊 Fluxo de Dados

```
┌─────────────────────────────────────┐
│  Scraping InvestSite                │ (35-45 segundos)
├─────────────────────────────────────┤
│  ↓ HTML                             │
├─────────────────────────────────────┤
│  Extração de Dados                  │
├─────────────────────────────────────┤
│  ↓ DataFrame pandas                 │
├─────────────────────────────────────┤
│  Cálculo de Volatilidade (yfinance) │ (5-10 minutos)
├─────────────────────────────────────┤
│  ↓ DataFrame com volatilidade       │
├─────────────────────────────────────┤
│  Filtragem de Negócio               │
├─────────────────────────────────────┤
│  ↓ DataFrame filtrado               │
├─────────────────────────────────────┤
│  Enriquecimento com Detalhes        │ (5-10 minutos)
├─────────────────────────────────────┤
│  ↓ DataFrame final                  │
├─────────────────────────────────────┤
│  Salvar em Excel                    │ (10 segundos)
└─────────────────────────────────────┘
```

---

## 🧪 Testando Componentes

Cada documento tem exemplos de teste:

| Componente | Exemplo | Arquivo |
|-----------|---------|---------|
| Adapter de Scraping | `test_single_adapter.py` | EXEMPLOS_USO.md |
| Serviços | `test_services.py` | EXEMPLOS_USO.md |
| Volatilidade | `test_volatility.py` | EXEMPLOS_USO.md |
| Com Mocks | `test_with_mocks.py` | EXEMPLOS_USO.md |

---

## 📚 Recursos Externos

- [Python 3.11+ Docs](https://docs.python.org/3.11/)
- [Selenium Docs](https://www.selenium.dev/documentation/)
- [Pandas Docs](https://pandas.pydata.org/docs/)
- [yfinance Docs](https://github.com/ranaroussi/yfinance)
- [Hexagonal Architecture](https://en.wikipedia.org/wiki/Hexagonal_architecture_(software))

---

## 💬 Convenções de Código

### Nomenclatura
- **Classes**: `PascalCase` (ex: `StockFilterService`)
- **Funções/métodos**: `snake_case` (ex: `apply_filters()`)
- **Constantes**: `UPPER_SNAKE_CASE` (ex: `WAIT_TIME_AFTER_FILTER`)

### Docstrings
Usamos docstrings para documentar classes e funções:

```python
class MyClass:
    """Uma linha resumida.
    
    Descrição mais longa se necessário.
    
    Attributes:
        attr1: Descrição do atributo
    """
    
    def my_method(self, param1: str) -> bool:
        """Uma linha resumida.
        
        Args:
            param1: Descrição do parâmetro
        
        Returns:
            Descrição do retorno
        
        Raises:
            ValueError: Quando algo está errado
        """
```

---

## 🚨 Reportar Problemas

Se encontrar problema:

1. **Verificar** documentação relevante
2. **Consultar** SETUP_DEPLOYMENT.md seção "Troubleshooting"
3. **Revisar** logs (arquivo `app.log`)
4. **Executar** com `WEBDRIVER_HEADLESS = False` para debug visual
5. **Consultar** GUIA_DESENVOLVIMENTO.md para detalhes técnicos

---

## 🎓 Learning Path Recomendado

**Iniciante:**
1. README.md
2. SETUP_DEPLOYMENT.md
3. Executar `python app/main.py`

**Intermediário:**
1. GUIA_DESENVOLVIMENTO.md
2. EXEMPLOS_USO.md
3. Modificar `constants.py`

**Avançado:**
1. ARQUITETURA.md
2. Estudar código-fonte
3. Adicionar novos componentes
4. Escrever testes

---

## 📝 Checklist de Setup

- [ ] Python 3.11+ instalado
- [ ] Repositório clonado
- [ ] Ambiente virtual criado
- [ ] Dependências instaladas (`pip install -r requirements.txt`)
- [ ] Firefox instalado
- [ ] `constants.py` configurado com seu path
- [ ] Execução de teste OK (`python app/test_single_adapter.py`)
- [ ] Execução principal OK (`python app/main.py`)

---

## 📞 Contato

Para dúvidas sobre este projeto:
- Revisar a documentação relevante
- Consultar exemplos em EXEMPLOS_USO.md
- Debugar com `WEBDRIVER_HEADLESS = False`

---

**Última atualização**: Maio 2025

**Versão da Documentação**: 2.0

**Status**: ✅ Completo e Atualizado

---

Boa sorte! 🚀 Se precisar de ajuda, toda resposta está em um dos documentos acima! 

