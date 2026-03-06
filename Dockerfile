FROM python:3.12-slim

# Instalace systémových závislostí pro SQLite a kompilaci knihoven
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libssl-dev \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Kopírujeme requirements do kořene a instalujeme
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopírujeme vše ostatní (včetně main.py a ramky.db) do kořene
COPY . .

# Spuštění přímo z kořenového adresáře
CMD ["python", "main.py"]