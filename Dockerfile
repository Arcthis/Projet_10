FROM python:3.11-slim

# Installer dépendances système utiles (lib pour Excel, etc.)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Installer les librairies Python nécessaires
RUN pip install --no-cache-dir \
    pandas \
    numpy \
    duckdb \
    openpyxl

# Vérifier
RUN python -c "import pandas, numpy, duckdb, openpyxl"
