# Basis-Image: schlankes Python-Image
FROM python:3.13-slim

# Installiere notwendige Systempakete
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# Setze das Arbeitsverzeichnis
WORKDIR /app

# Kopiere die Abhängigkeitsdatei (requirements.txt) in das Image
COPY requirements.txt .

# Installiere Python-Abhängigkeiten
RUN cat requirements.txt && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Kopiere den restlichen Code des Bots in das Image
COPY . .

# Starte den Python-Scheduler
CMD ["python", "bot.py"]