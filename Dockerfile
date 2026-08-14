FROM python:3.14-slim

# Evita .pyc e garante logs em tempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Dependências de sistema (ajuste conforme sua stack, ex: libpq para postgres)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Instala dependências Python primeiro (aproveita cache do Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o resto do código
COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver"]
