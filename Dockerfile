# E2E Test Docker Image
# Based on Python 3.11-slim with Playwright and Chromium

FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright with Chromium and its dependencies
RUN playwright install --with-deps chromium

# Copy project files
COPY . .

# Create artifacts directory
RUN mkdir -p /app/artifacts/screenshots /app/artifacts/traces

# Set default environment variables (can be overridden at runtime)
ENV HEADLESS=true \
    TIMEOUT=30000

# Default command: run pytest with HTML and JUnit reports
CMD ["pytest", \
     "--junitxml=/app/artifacts/junit.xml", \
     "--html=/app/artifacts/report.html", \
     "--self-contained-html", \
     "-v"]
