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

# Copy everything
COPY / /app/
COPY frontend/ /app/frontend/
COPY requirements.txt /app/

RUN mkdir -p /app/downloads

VOLUME ["/app/downloads"]

# Expose port
EXPOSE 8000

# Run the server
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
