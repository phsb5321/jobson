# Use an official Python runtime as a parent image
FROM python:3.10-slim AS base

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/usr/src/app

# Set the working directory in the container
WORKDIR /usr/src/app

# Install system dependencies
RUN apt-get update && \
    apt-get install --no-install-recommends -y netcat-openbsd && \
    rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false

# Copy the pyproject.toml and optionally poetry.lock files
COPY pyproject.toml poetry.lock* ./

# Install project dependencies
RUN poetry install --no-root --no-dev --no-interaction --no-ansi

# Copy the current directory contents into the container at /usr/src/app
COPY . .

EXPOSE 80

# Set the default command to run the Streamlit app on port 3000
CMD ["streamlit", "run", "public/main.py", "--server.port=80"]
