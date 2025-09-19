# Base image
FROM python:3.12-slim

# Set workdir
WORKDIR /app

# Prevent Python from writing pyc files and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install system deps required to build some Python wheels (Pillow, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    libssl-dev \
    libffi-dev \
    zlib1g-dev \
    libjpeg-dev \
    libpng-dev \
    libfreetype6-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip/setuptools/wheel so pip can fetch manylinux wheels when available
RUN python -m pip install --upgrade pip setuptools wheel

# Install pip dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . /app

# Expose port used by uvicorn
EXPOSE 8000

# Default command
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
