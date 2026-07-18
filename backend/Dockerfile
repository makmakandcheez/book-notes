FROM python:3.14-slim

COPY ./requirements.txt /app/

WORKDIR /app/

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY ./app /app

CMD ["fastapi", "run", "/app/app/main.py", "--host", "0.0.0.0", "--port", "8000"]