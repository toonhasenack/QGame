# QGame

Simpel quantum spelletje

## Hoe te runnen?

Volg de onderstaande stappen om de Django-webserver voor QGame te starten en de applicatie in je lokale omgeving te bekijken.

### 1. Installeren van Dependencies

Zorg ervoor dat alle benodigde dependencies correct zijn geïnstalleerd. Dit kun je doen door het `requirements.txt`-bestand te gebruiken. Typ het volgende commando in de terminal om de vereiste packages te installeren:

```bash
pip install -r requirements.txt
```

### 2. De Webserver Starten

Start de Django-webserver met het volgende commando:

```bash
python manage.py runserver
```

Je kunt nu je webbrowser openen en naar http://127.0.0.1:8000 gaan om de applicatie te bekijken op je lokale server.

### 3. Het Scoreboard Bekijken

Om het scoreboard te bekijken, ga je naar de volgende URL in je webbrowser:

```arduino
http://127.0.0.1:8000/leaderboard
```

Deze URL toont het scoreboard van het spelletje.

### 4. De Database Flushen

Als je de database wilt flushen (bijvoorbeeld om alle gegevens te verwijderen en opnieuw te beginnen), gebruik dan het volgende commando:

```bash
python manage.py flush
```
Let op: Dit commando verwijdert alle gegevens uit de database en kan niet worden ongedaan gemaakt. Gebruik dit commando met voorzichtigheid.
