FROM python:3.10-slim-bullseye

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    git \
    openssh-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app

# Create app directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files
COPY . .

# Make the gunicorn startup script executable
RUN chmod +x /app/start_gunicorn.sh

# Expose port
EXPOSE 8000

# Set working directory to Django project
WORKDIR /app/vajrabox

# Default command - use the startup script instead of direct gunicorn
CMD ["/app/start_gunicorn.sh"]