# Dockerfile — usa Python 3.11
FROM python:3.11-slim

# Metadatos
LABEL maintainer="tu@correo.com"

# Evita buffers en logs
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copia archivos y solo instala dependencias
COPY requirements.txt /app/requirements.txt
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc libffi-dev libssl-dev \
 && pip install --upgrade pip \
 && pip install -r /app/requirements.txt \
 && apt-get remove -y build-essential gcc \
 && apt-get autoremove -y \
 && rm -rf /var/lib/apt/lists/*

# Copia el resto del código
COPY . /app

# Otorga permisos (no root ideal)
RUN useradd --create-home appuser && chown -R appuser:appuser /app
USER appuser

# Puerto no necesario, bot usa polling (no web)
# Comando por defecto
CMD ["python", "bot_with_paywall.py"]
