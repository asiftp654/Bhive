FROM python:3.10-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app


# Installing dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \ 
        gcc \
        dos2unix \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

COPY entrypoint.sh /entrypoint.sh
COPY wait_for_db.py /app/wait_for_db.py
RUN chmod +x /entrypoint.sh && \
    chmod +x /app/wait_for_db.py && \
    # Convert Windows line endings to Unix line endings for all shell scripts
    dos2unix /entrypoint.sh

# Create a non-root user and set up directories
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app \
    && mkdir -p /app/celerybeat-schedule-data \
    && chown -R app:app /app/celerybeat-schedule-data

USER app

EXPOSE 8000

