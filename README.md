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

Wähle eine der beiden Optionen:

- **Docker Setup (empfohlen):** Docker und Docker Compose installiert
- **Lokale Entwicklung:** Python 3.8+, pip und git

### Quick Start mit Docker

Die einfachste Variante - alles läuft in Containern.

#### Schritt 1: Repository klonen

```bash
git clone https://github.com/AndreiButalov/videoflix_backend.git
cd videoflix_backend
```

#### Schritt 2: Umgebungsvariablen kopieren

```bash
cp .env.template .env
```

#### Schritt 3: .env-Datei konfigurieren

Öffne die `.env`-Datei und fülle diese wichtigen Variablen aus:

```env
SECRET_KEY=dein-sicherer-secret-key
DEBUG=False
FRONTEND_URL=http://localhost:3000

# E-Mail für Account-Aktivierung
EMAIL_HOST_USER=deine-email@gmail.com
EMAIL_HOST_PASSWORD=dein-app-passwort

# Datenbank
DATABASE_URL=postgresql://user:password@db:5432/videoflix
```

#### Schritt 4: Docker Compose starten

```bash
docker-compose up --build
```

Das Backend ist dann erreichbar unter: **http://localhost:8000**

Die erste Initialisierung kann 2-3 Minuten dauern. Warte bis die Meldung erscheint, dass der Server läuft.

---

### Lokale Installation (Entwicklung ohne Docker)

Für lokale Entwicklung und Testing.

#### Schritt 1: Repository klonen

```bash
git clone https://github.com/AndreiButalov/videoflix_backend.git
cd videoflix_backend
```

#### Schritt 2: Virtuelle Umgebung erstellen

**Windows:**
```bash
python -m venv env
env\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv env
source env/bin/activate
```

Nach erfolgreicher Aktivierung siehst du `(env)` am Anfang deiner Eingabezeile.

#### Schritt 3: Abhängigkeiten installieren

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Das installiert alle notwendigen Pakete wie Django, Django REST Framework, PostgreSQL-Driver, etc.

#### Schritt 4: Umgebungsvariablen kopieren und konfigurieren

```bash
cp .env.template .env
```

Öffne `.env` und fülle folgende Werte aus:

```env
SECRET_KEY=dein-sicherer-secret-key
DEBUG=True
FRONTEND_URL=http://localhost:3000

# E-Mail für Account-Aktivierung
EMAIL_HOST_USER=deine-email@gmail.com
EMAIL_HOST_PASSWORD=dein-app-passwort

# Datenbank (SQLite für lokale Entwicklung)
DATABASE_URL=sqlite:///db.sqlite3
```

#### Schritt 5: Datenbank initialisieren

```bash
python manage.py migrate
```

Das erstellt alle notwendigen Datenbanktabellen.

#### Schritt 6: Admin-Benutzer erstellen (optional)

```bash
python manage.py createsuperuser
```

Folge den Anweisungen um einen Admin-Account zu erstellen. Danach kannst du auf `http://localhost:8000/admin` zugreifen.

#### Schritt 7: Server starten

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
