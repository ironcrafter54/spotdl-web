# Use official Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && \
    apt-get install -y ffmpeg git curl && \
    apt-get clean

# Install spotDL via pip
RUN pip install --no-cache-dir spotdl fastapi uvicorn[standard]

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything
COPY . /app/

RUN mkdir -p /app/downloads

VOLUME ["/app/downloads"]

# Expose port
EXPOSE 8000

# Test imports before running
RUN python test_import.py

# Run the server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
