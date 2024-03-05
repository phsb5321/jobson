# Base image with your specific Python version
FROM python:3.10-slim AS base

# Set essential environment variables to:
# - Ensure Python output goes straight to the terminal (without buffering)
# - Prevent Python from generating .pyc files
ENV PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1
# Set Python PATH to find the installed packages
PYTHONPATH=/usr/src/app

# Set the working directory to /usr/src/app
WORKDIR /usr/src/app

# Install poetry using pip and update pip to the latest version
# We use `--no-cache-dir` to keep the image small
# The virtual environment is not needed in the container,
# so we disable its creation.
RUN pip install --no-cache-dir --upgrade pip &&
  pip install --no-cache-dir poetry &&
  poetry config virtualenvs.create false

# Copy only Poetry configuration files first to cache this layer,
# this layer will be rebuilt only if pyproject.toml or poetry.lock change.
COPY pyproject.toml poetry.lock* ./

# Install the project dependencies without dev dependencies for production
RUN poetry install --no-root --no-dev --no-interaction --no-ansi

# Copy your application code to the /usr/src/app folder in the container
COPY . .

# Use gunicorn as the entry point for running the application in production
# Adjust the number of workers and threads as necessary
# Replace `app.main:app` with your application's module and variable
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app.main:app"]
