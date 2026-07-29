FROM python:3.14-slim

COPY --from=ghcr.io/astral-sh/uv:0.11.32 /uv /uvx /bin/

WORKDIR /app

COPY ./backend/pyproject.toml ./backend/uv.lock ./
RUN uv sync --frozen --no-install-project

COPY ./backend .
RUN uv sync --frozen

CMD ["uv", "run", "fastapi", "run", "/app/app/main.py", "--host", "0.0.0.0", "--port", "8000"]