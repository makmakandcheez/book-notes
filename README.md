# Multi-Container Note-Taker

A full-stack application for note-taking with a FastAPI backend, a Postgres database, and Docker contianerization. It features user creation and secure login with JWT token authentication.

## Project Structure

```
book-notes/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── __init__.py
│   │   │       ├── dependencies.py
│   │   │       └── endpoints/
│   │   │           ├── __init__.py
│   │   │           ├── auth.py
│   │   │           ├── books.py
│   │   │           ├── notes.py
│   │   │           └── users.py
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── config.py
│   │   │   ├── database.py
│   │   │   └── security.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── book.py
│   │   │   ├── note.py
│   │   │   ├── refresh_token.py
│   │   │   └── user.py
│   │   ├── repositories/
│   │   │   ├── __init__.py
│   │   │   ├── book_repo.py
│   │   │   ├── note_repo.py
│   │   │   ├── refresh_token_repo.py
│   │   │   └── user_repo.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── book.py
│   │   │   ├── note.py
│   │   │   └── user.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py
│   │   │   ├── book_service.py
│   │   │   ├── note_service.py
│   │   │   └── user_service.py
│   │   ├─ utils/
│   │   │  └── __init__.py
│   │   ├── __init__.py
│   │   └─ main.py
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   ├── integration/
│   │   │   ├── __init__.py
│   │   │   ├── test_auth_api.py
│   │   │   ├── test_dependencies.py
│   │   │   ├── test_notes_api.py
│   │   │   └── test_users_api.py
│   │   └── unit/
│   │       ├── __init__.py
│   │       ├── core/
│   │       │   ├── __init__.py
│   │       │   └── test_security.py
│   │       ├── repositories/
│   │       │   ├── __init__.py
│   │       │   ├── test_note_repo.py
│   │       │   └── test_user_repo.py
│   │       └── services/
│   │           ├── __init__.py
│   │           ├── test_auth_service.py
│   │           ├── test_note_service.py
│   │           └── test_user_service.py
│   ├── .python-version
│   ├── Dockerfile
│   ├── pyproject.toml
│   ├── requirements.txt
│   └── uv.lock
├── database/
│   └── init.sql
├── docker-compose.yml                           # postgres + backend
├── LICENSE
├── README.md
├── .dockerignore
└── .ignore

```


## Getting Started
---
### Using Docker
1. Make sure [Docker](https://www.docker.com/get-started/) and [Docker Compose](https://docs.docker.com/compose/install/) installed.
2. Start application
```
docker compose -f docker-compose.yml up -d
```
Docker will start containers based on the images for the backend and the Postgres database. 

