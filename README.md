# Book Notes

A full-stack application for note-taking with a FastAPI backend, a PostgreSQL database, and Docker containerization. It features user creation and secure login with JWT token authentication.

## Project Structure

```text
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
│   │   ├── utils/
│   │   │   └── __init__.py
│   │   ├── __init__.py
│   │   └── main.py
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
├── docker-compose.yml
├── LICENSE
├── README.md
├── .dockerignore
└── .ignore
```


## Getting Started
---

### Using Docker

1. Make sure [Docker](https://www.docker.com/get-started/) and [Docker Compose](https://docs.docker.com/compose/install/) are installed.
2. Start the application:

```bash
docker compose -f docker-compose.yml up -d
```


Docker will start containers based on the images for the backend and the PostgreSQL database.

To stop the application:

```bash
docker compose -f docker-compose.yml down
```

To stop the containers and remove the database volume:

```bash
docker compose -f docker-compose.yml down -v
```

> Removing the volume will delete the PostgreSQL data stored by the container.

### Environment Variables

The backend requires environment variables for configuration and security.

Create a `.env` file in the `backend/` directory:

```env
DATABASE_URL=postgresql+asyncpg://postgres:password@db:5432/book_notes
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

Do not commit your `.env` file or production secrets to version control.

---

## Architecture

The backend follows a layered architecture that separates HTTP handling, business logic, database access, and data models.

```text
Client
  │
  ▼
Endpoints
  │
  ▼
Services
  │
  ▼
Repositories
  │
  ▼
SQLAlchemy Models
  │
  ▼
PostgreSQL
```

### API Layer

The `api` package contains the HTTP endpoints and request dependencies.

Endpoints are responsible for:

* Receiving and validating HTTP requests
* Calling the appropriate service
* Returning the appropriate response
* Handling authentication and authorization dependencies

### Service Layer

The `services` package contains application and business logic.

Services coordinate operations between the API and repository layers without directly handling HTTP requests.

For example, authentication is handled by the authentication service rather than being implemented directly inside an endpoint.

### Repository Layer

The `repositories` package handles database operations.

Repositories provide an abstraction over SQLAlchemy and are responsible for operations such as:

* Creating records
* Retrieving records
* Updating records
* Deleting records
* Filtering database queries

This keeps database-specific logic separate from application logic.

### Models and Schemas

SQLAlchemy models in `models/` represent database entities, while Pydantic schemas in `schemas/` define the data accepted and returned by the API.

This separation allows database models and API representations to evolve independently.

---

## Authentication

Authentication uses JSON Web Tokens (JWT) with separate access and refresh tokens.

### Access Tokens

Access tokens are short-lived tokens used to authenticate API requests.

Authenticated requests include the token in the `Authorization` header:

```http
Authorization: Bearer <access-token>
```

The API validates the token and retrieves the associated user before allowing access to protected resources.

### Refresh Tokens

Refresh tokens provide a way to obtain a new access token without requiring the user to log in again.

Refresh tokens are stored in the database using a unique token identifier and a hash of the token rather than storing the raw token itself.

This allows refresh tokens to be revoked and invalidated while avoiding storage of usable token credentials in plaintext.

### Password Security

User passwords are never stored directly in the database. Passwords are hashed before being persisted and verified against their stored hashes during authentication.

---

## API

The API is built with FastAPI and provides endpoints for authentication, users, and notes.

The API is versioned under `/api/v1`.

### Authentication

| Method | Endpoint              | Description                                    |
| ------ | --------------------- | ---------------------------------------------- |
| `POST` | `/auth/signup`        | Create a new user                              |
| `POST` | `/auth/token`         | Authenticate a user and obtain an access token |
| `POST` | `/auth/refresh-token` | Refresh an expired access token                |

### Notes

| Method   | Endpoint      | Description           |
| -------- | ------------- | --------------------- |
| `GET`    | `/notes/`     | Retrieve notes        |
| `POST`   | `/notes/`     | Create a note         |
| `GET`    | `/notes/{id}` | Retrieve a note by ID |
| `PATCH`  | `/notes/{id}` | Update a note         |
| `DELETE` | `/notes/{id}` | Delete a note         |

### Users

| Method   | Endpoint            | Description                               |
| -------- | ------------------- | ----------------------------------------- |
| `GET`    | `/users/`           | Retrieve users  with pagination and filtering                          |
| `GET`    | `/users/me`         | Retrieve the currently authenticated user |
| `GET`    | `/users/{id}`       | Retrieve a user by ID                     |
| `PATCH`  | `/users/{id}`       | Update a user                             |
| `DELETE` | `/users/{id}`       | Delete a user                             |
| `GET`    | `/users/{id}/notes` | Retrieve a user's publicly visible notes  |

### General

| Method | Endpoint | Description                      |
| ------ | -------- | -------------------------------- |
| `GET`  | `/`      | Retrieve API information         |
| `GET`  | `/about` | Retrieve application information |



Protected endpoints require a valid JWT access token in the `Authorization` header:

```http
Authorization: Bearer <access-token>
```

Access tokens are short-lived and can be renewed using a refresh token through `/auth/refresh-token`.

Refresh tokens are persisted securely in the database using a hash of the token rather than storing the raw token.


---

## Testing


The project uses `pytest` for automated testing and separates tests into unit and integration tests.

### Unit Tests

Unit tests focus on individual components in isolation, including:

* Security and JWT functionality
* Authentication services
* User services
* Note services
* Repository operations

### Integration Tests

Integration tests verify that multiple application components work together correctly.

These tests cover areas such as:

* Authentication endpoints
* User endpoints
* Note endpoints
* API dependencies
* Database interactions

Run the test suite from the `backend/` directory:

```bash
uv run pytest
```

---

## Technologies
* **Python**
* **FastAPI**
* **SQLAlchemy**
* **Pydantic**
* **PostgreSQL**
* **Docker**
* **Docker Compose**
* **JWT**
* **Pytest**
* **uv**

---

## Development

The backend is managed using `uv` for Python dependency and environment management.

From the `backend/` directory, install dependencies with:

```bash
uv sync
```

Run the FastAPI development server with:

```bash
uv run fastapi dev app/main.py
```

The API can then be accessed locally at:

```text
http://localhost:8000
```

FastAPI's interactive API documentation is available at:

```text
http://localhost:8000/docs
```

---

## Future Improvements

Potential future improvements include:

* Frontend client for interacting with the API
* Book metadata integration
* Rich-text note editing
* Note search and filtering
* Improved pagination and sorting
* Automated CI/CD
* Production deployment

---

## License

This project is licensed under the terms of the MIT License. See [`LICENSE`](LICENSE) for more information.
