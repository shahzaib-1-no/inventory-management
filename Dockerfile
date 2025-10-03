# Base image
FROM python:3.10-slim

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements folder
COPY requirements/ /app/requirements/

# Install dev dependencies
RUN pip install --upgrade pip
RUN pip install -r /app/requirements/dev.txt

# Copy project files
COPY . /app

# Expose port
EXPOSE 8000

# Default command (run Django dev server)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
