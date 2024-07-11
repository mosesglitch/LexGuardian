# Build stage
FROM python:3.11-slim as builder

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry

# Set the working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml poetry.lock* ./

# Install dependencies
ENV POETRY_HTTP_TIMEOUT=3600
RUN poetry config virtualenvs.create false \
    && poetry config installer.max-workers 10 \
    && poetry config installer.parallel true \
    && poetry install --no-interaction --no-ansi --no-root

# Copy the rest of the application
COPY . .

# Install the project
RUN poetry install --no-interaction --no-ansi

# Runtime stage
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy installed packages and application from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /app /app

# Install runtime system dependencies if any
RUN apt-get update && apt-get install -y \
    # Add any runtime dependencies here \
    && rm -rf /var/lib/apt/lists/*

# Expose Streamlit port
EXPOSE 8501

# Run the application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
