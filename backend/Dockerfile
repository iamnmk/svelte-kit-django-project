FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY backend /app/backend

ENV NOTES_DATA_FILE=/data/notes.json
ENV CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,http://145.241.154.193:3000

EXPOSE 8000

CMD ["python", "/app/backend/manage.py", "runserver", "0.0.0.0:8000"]

