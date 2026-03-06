FROM python:3.12-slim

# Instalace závislostí
RUN apt-get update && apt-get install -y \
    gcc g++ libssl-dev sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Instalace knihoven přímo v kořenu
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopírování skriptů do kořene
COPY . .

# Spuštění z kořene
CMD ["python", "main.py"]