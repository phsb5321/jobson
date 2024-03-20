# Base image with your specific Python version
FROM python:3.10-slim AS base

# Set essential environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONPATH=/usr/src/app

# Set the working directory to /usr/src/app
WORKDIR /usr/src/app

# Install system dependencies
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

# Install poetry using pip and update pip to the latest version
RUN pip install --no-cache-dir --upgrade pip &&
  pip install --no-cache-dir poetry &&
  poetry config virtualenvs.create false

# Copy only Poetry configuration files first to cache this layer
COPY pyproject.toml poetry.lock* ./

# Install the project dependencies
RUN poetry install --no-root --no-dev --no-interaction --no-ansi

# Copy your application code to the /usr/src/app folder in the container
COPY . .

# Streamlit specific stage
FROM base AS streamlit
CMD ["streamlit", "run", "public/main.py", "--server.port=8501", "--server.address=0.0.0.0"]

# Server specific stage
FROM base AS server
CMD ["python", "-m", "app.main"]

# Final stage which decides which app to run based on an environment variable
FROM base AS final
ARG APP_TYPE=server

# Copy the application from the relevant stage
COPY --from=${APP_TYPE} /usr/src/app /usr/src/app

# Use an environment variable to switch between the Streamlit app and the server app
ENTRYPOINT [ "sh", "-c", "if [ \"$APP_TYPE\" = 'streamlit' ]; then streamlit run public/main.py --server.port=8501 --server.address=0.0.0.0; else python -m app.main; fi" ]
