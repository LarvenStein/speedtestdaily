# Basis-Image: schlankes Python-Image
FROM python:3.11-slim

# Installiere notwendige Systempakete
RUN apt-get update && apt-get install -y \
    cron \
    && rm -rf /var/lib/apt/lists/*

# Setze das Arbeitsverzeichnis
WORKDIR /app

# Kopiere die Abhängigkeitsdatei (requirements.txt) in das Image
COPY requirements.txt .

# Installiere Python-Abhängigkeiten
RUN pip install --no-cache-dir -r requirements.txt

# Kopiere den restlichen Code des Bots in das Image
COPY . .

# Erstelle die Cronjob-Datei
RUN echo "0 0 * * * python /app/bot.py >> /var/log/cron.log 2>&1" > /etc/cron.d/mastodon-bot-cron

# Setze die Berechtigungen für die Cronjob-Datei
RUN chmod 0644 /etc/cron.d/mastodon-bot-cron

# Registriere die Cronjobs
RUN crontab /etc/cron.d/mastodon-bot-cron

# Erstelle ein Logfile für Cron
RUN touch /var/log/cron.log

# Starte den Cron-Dienst und bleibe im Vordergrund (damit der Container läuft)
CMD ["cron", "-f"]