# Videoflix Backend

## Description

This is the backend for the Videoflix streaming platform, developed with Django and Django REST Framework. It provides authentication, video management, and API endpoints for the frontend application.

## Features

- User registration and account activation via email
- JWT-based authentication with cookies
- Password reset functionality
- Video upload and management
- RESTful API for all operations

## Technologies

- **Django** 6.0.3
- **Django REST Framework** 3.16.1
- **Django Simple JWT** 5.5.1
- **Redis** for caching
- **PostgreSQL** as database (SQLite for development)
- **Docker** for containerization

## Installation

### Prerequisites

- **Docker Setup (recommended):** Docker and Docker Compose installed
- **Local Development:** Python, pip and git

### Quick Start with Docker


#### Step 1: Clone repository

```bash
git clone https://github.com/AndreiButalov/videoflix_backend.git
cd videoflix_backend
```

#### Step 2: Copy environment variables

```bash
cp .env.template .env
```

#### Step 3: Configure .env file

Open the `.env` file and fill in these important variables:

```env
SECRET_KEY=your-secure-secret-key
DEBUG=False
FRONTEND_URL=http://localhost:3000

# Email for account activation
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Database
DATABASE_URL=postgresql://user:password@db:5432/videoflix
```

#### Step 4: Start Docker Compose

```bash
docker-compose up --build
```

The backend is then accessible at: **http://localhost:8000**

The first initialization can take 2-3 minutes. Wait until the message appears that the server is running.

---

### Local Installation (Development without Docker)

For local development and testing.

#### Step 1: Clone repository

```bash
git clone https://github.com/AndreiButalov/videoflix_backend.git
cd videoflix_backend
```

#### Step 2: Create virtual environment

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

After successful activation you will see `(env)` at the beginning of your command line.

#### Step 3: Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This installs all necessary packages like Django, Django REST Framework, PostgreSQL driver, etc.

#### Step 4: Copy and configure environment variables

```bash
cp .env.template .env
```

Open `.env` and fill in the following values:

```env
SECRET_KEY=your-secure-secret-key
DEBUG=True
FRONTEND_URL=http://localhost:3000

# Email for account activation
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Database (SQLite for local development)
DATABASE_URL=sqlite:///db.sqlite3
```

#### Step 5: Initialize database

```bash
python manage.py migrate
```

This creates all necessary database tables.

#### Step 6: Create admin user (optional)

```bash
python manage.py createsuperuser
```

Follow the instructions to create an admin account. You can then access the admin panel at `http://localhost:8000/admin`.

#### Step 7: Start server

```bash
python manage.py runserver
```

The backend runs at: **http://localhost:8000**

---

### Troubleshooting

**"ModuleNotFoundError" or "No module named"**
- Make sure the virtual environment is activated (Windows: `env\Scripts\activate`)
- Run `pip install -r requirements.txt`

**"Connection refused" with database**
- With Docker: Wait until all containers are fully started
- Locally: Make sure PostgreSQL is running (if not using SQLite)

**Port 8000 already in use**
```bash
python manage.py runserver 8001
```

**Email doesn't work**
- Check `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` in `.env`
- For Gmail: Use an app password, not your regular password

## API Endpoints

### Authentication

- `POST /api/register/` - User registration
- `GET /api/activate/<uidb64>/<token>/` - Account activation
- `POST /api/login/` - Login
- `POST /api/logout/` - Logout
- `POST /api/token/refresh/` - Token refresh
- `POST /api/password_reset/` - Request password reset
- `POST /api/password_confirm/<uidb64>/<token>/` - Confirm password reset

### Videos

- `GET /api/video/` - List videos
- `GET /api/video/<movie_id>/<resolution>/index.m3u8` - Request HLS master playlist
- `GET /api/video/<movie_id>/<resolution>/<segment>/` - Request HLS segment

## Usage

### Development

- Run tests: `python manage.py test`
- Linting: Use Black or Flake8
- API documentation: Use Swagger or DRF browsable API

### Production

- Use Gunicorn as WSGI server
- Serve static files with WhiteNoise
- Redis for caching and sessions

## Project Structure

```
videoflix_backend/
├── auth_app/          # Authentication app
├── videoflix_app/     # Main video app
├── core/              # Django core settings
├── media/             # Uploaded files
├── static/            # Static files
├── requirements.txt   # Python dependencies
├── docker-compose.yml # Docker configuration
└── manage.py          # Django management script
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
