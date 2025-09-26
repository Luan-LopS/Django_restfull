FROM python:3.11-slim AS python-base

# Variáveis de ambiente para otimizar Python, pip e Poetry
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=2.2.0 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv" \
    PATH="/opt/poetry/bin:/opt/pysetup/.venv/bin:$PATH"

# Instala dependências do sistema necessárias para Poetry, build e PostgreSQL
RUN apt-get update && apt-get install --no-install-recommends -y \
        curl \
        build-essential \
        libpq-dev \
        gcc \
    && rm -rf /var/lib/apt/lists/*

# Instala o Poetry na versão especificada
RUN curl -sSL https://install.python-poetry.org | python3 -

# Instala psycopg2 via pip (pode ser necessário para evitar problemas com Poetry)
RUN pip install psycopg2

# Define diretório de trabalho para copiar os arquivos de configuração do Poetry
WORKDIR $PYSETUP_PATH

# Copia arquivos do Poetry para aproveitar cache do Docker
COPY poetry.lock pyproject.toml README.md ./

# Instala somente dependências principais, sem dev e sem instalar o projeto
RUN poetry install --only main --no-root --no-interaction --no-ansi

# Agora copia todo o código da aplicação para /app
WORKDIR /app
COPY . /app/

# Expõe porta padrão do Django
EXPOSE 8000

# Comando padrão para rodar o servidor de desenvolvimento Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
