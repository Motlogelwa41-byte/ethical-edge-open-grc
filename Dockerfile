# Use an official lightweight Python runtime
FROM python:3.11-slim

# Set system environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV WORKDIR=/workspace

WORKDIR $WORKDIR

# Install system dependencies needed for Postgres and building packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application files
COPY . .

# Expose the port your unified main.py runs on
EXPOSE 8000

# Run the Uvicorn application server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
