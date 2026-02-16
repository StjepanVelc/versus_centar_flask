# Versus Centar – Flask Web Application

Production-structured Flask web application for managing courses, events, registrations and administrative operations.

Designed with modular architecture, database migrations, authentication security and deployment-ready configuration.

---

## Tech Stack

- Python 3
- Flask (Blueprint pattern)
- SQLAlchemy ORM
- PostgreSQL (Supabase)
- Flask-Migrate (Alembic)
- Flask-WTF (CSRF Protection)
- Flask-Limiter
- Bootstrap 5

---

## Core Features

- Admin authentication (hashed passwords, session-based)
- Role-based access control
- Course & Event CRUD
- Event registration system
- Contact form handling
- Database migrations
- Backup functionality

---

## Architecture

- Modular Blueprint structure
- Centralized extensions layer
- Environment-based configuration (dev/prod separation)
- Secure `.env` configuration
- Production-oriented project structure

---

## Database

PostgreSQL with version-controlled migrations using Flask-Migrate.


---

## Security

- scrypt password hashing
- CSRF protection
- Rate limiting
- Session validation
- Admin route protection

---

## Deployment

- Render (application)
- Supabase (database)
- Git/GitHub CI-ready structure

---

## Author

Stjepan Velc
