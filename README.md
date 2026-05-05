# Videoflix Backend

## Beschreibung

Dies ist das Backend für die Videoflix-Plattform, entwickelt mit Django und Django REST Framework. Es bietet Authentifizierung, Video-Management und API-Endpunkte für die Frontend-Anwendung.

## Features

- Benutzerregistrierung und -aktivierung per E-Mail
- JWT-basierte Authentifizierung mit Cookies
- Passwort-Reset-Funktionalität
- Video-Upload und -Management
- RESTful API für alle Operationen

## Technologien

- **Django** 6.0.3
- **Django REST Framework** 3.16.1
- **Django Simple JWT** 5.5.1
- **Redis** für Caching
- **PostgreSQL** als Datenbank (mit SQLite für Entwicklung)
- **Docker** für Containerisierung

## Installation

### Voraussetzungen

- Docker und Docker Compose (empfohlen)
- Für lokale Installation: Python 3.8+

### Umgebungsvariablen einrichten

**Wichtig:** Vor dem Start das `.env`-Template kopieren:

```bash
cp .env.template .env
```

Dann die Variablen in `.env` anpassen:
- `SECRET_KEY` - Django Secret Key
- `EMAIL_HOST_USER` - E-Mail-Adresse für Versand
- `EMAIL_HOST_PASSWORD` - E-Mail App-Passwort
- Weitere Konfigurationen wie nötig

Siehe `.env.template` für alle verfügbaren Variablen.

### Docker Setup (empfohlen)

1. Repository klonen:
   ```bash
   git clone <repository-url>
   cd videoflix_backend
   ```

2. `.env`-Datei aus Template erstellen:
   ```bash
   cp .env.template .env
   ```

3. Variablen in `.env` konfigurieren (vor allem `FRONTEND_URL`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`)

4. Docker Compose starten:
   ```bash
   docker-compose up --build
   ```

Das Backend läuft dann unter `http://localhost:8000`

### Lokale Installation (optional)

Falls du lokal ohne Docker entwickeln möchtest:

1. Repository klonen:
   ```bash
   git clone <repository-url>
   cd videoflix_backend
   ```

2. `.env`-Datei aus Template erstellen:
   ```bash
   cp .env.template .env
   ```

3. Virtuelle Umgebung erstellen und aktivieren:
   ```bash
   python -m venv env
   env\Scripts\activate  # Windows
   # source env/bin/activate  # Linux/Mac
   ```

4. Abhängigkeiten installieren:
   ```bash
   pip install -r requirements.txt
   ```

5. Datenbank migrieren:
   ```bash
   python manage.py migrate
   ```

6. Server starten:
   ```bash
   python manage.py runserver
   ```

## API-Endpunkte

### Authentifizierung

- `POST /api/register/` - Benutzerregistrierung
- `GET /api/activate/<uidb64>/<token>/` - Kontoaktivierung
- `POST /api/login/` - Anmeldung
- `POST /api/logout/` - Abmeldung
- `POST /api/token/refresh/` - Token-Aktualisierung
- `POST /api/password_reset/` - Passwort-Reset anfordern
- `POST /api/password_confirm/<uidb64>/<token>/` - Passwort bestätigen

### Videos

- `GET /api/video/` - Videos auflisten
- `GET /api/video/<movie_id>/<resolution>/index.m3u8` - HLS-Master-Playlist anfordern
- `GET /api/video/<movie_id>/<resolution>/<segment>/` - HLS-Segment anfordern

## Verwendung

### Entwicklung

- Tests ausführen: `python manage.py test`
- Linting: Verwende Black oder Flake8
- API-Dokumentation: Verwende Swagger oder DRF browsable API

### Produktion

- Verwende Gunicorn als WSGI-Server
- Statische Dateien mit WhiteNoise servieren
- Redis für Caching und Sessions

## Projektstruktur

```
videoflix_backend/
├── auth_app/          # Authentifizierungs-App
├── videoflix_app/     # Haupt-App für Videos
├── core/              # Django-Kernsettings
├── media/             # Hochgeladene Dateien
├── static/            # Statische Dateien
├── requirements.txt   # Python-Abhängigkeiten
├── docker-compose.yml # Docker-Konfiguration
└── manage.py          # Django-Management-Script
```

## Beitrag

1. Fork das Repository
2. Erstelle einen Feature-Branch
3. Committe deine Änderungen
4. Pushe zum Branch
5. Erstelle einen Pull Request