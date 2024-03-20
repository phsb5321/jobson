# Base image with your specific Python version
FROM python:3.10-slim AS base

# Set essential environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONPATH=/usr/src/app

# Set the working directory to /usr/src/app
WORKDIR /usr/src/app

# Install system packages, pip, poetry, and supervisor
RUN apt-get update && apt-get install -y netcat-openbsd supervisor &&
  rm -rf /var/lib/apt/lists/* &&
  pip install --no-cache-dir --upgrade pip &&
  pip install --no-cache-dir poetry &&
  poetry config virtualenvs.create false

# Copy only necessary configuration files first to cache this layer
COPY pyproject.toml poetry.lock* ./

# Install the project dependencies
RUN poetry install --no-root --no-dev --no-interaction --no-ansi

# Copy your application code and configuration to the /usr/src/app folder in the container
COPY . .

# Supervisor configuration file
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
