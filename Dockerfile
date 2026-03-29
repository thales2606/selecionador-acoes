# Dockerfile para aplicação Python com suporte a CVM
FROM python:3.11-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    postgresql-client \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY app/requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar aplicação
COPY app .

# Criar diretório de logs
RUN mkdir -p /app/logs

# Expor porta para aplicação (se necessário)
EXPOSE 8000

# Definir variáveis de ambiente
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Comando padrão
CMD ["python", "main.py"]

