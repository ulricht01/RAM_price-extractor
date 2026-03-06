# 1. Použijeme stabilní a lehkou verzi Pythonu
FROM python:3.12-slim

# 2. Nastavení pracovního adresáře v kontejneru
WORKDIR /app

# 3. Instalace systémových závislostí (pokud tvůj main.py používá sqlite3)
RUN apt-get update && apt-get install -y \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# 4. Pokud máš soubor requirements.txt, odkomentuj tyto dva řádky:
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# 5. Zkopírování všech souborů z tvé složky do kontejneru
# (Včetně main.py, ramky.db a skriptů)
COPY . .

# 6. Spuštění tvého Python skriptu
CMD ["python", "main.py"]