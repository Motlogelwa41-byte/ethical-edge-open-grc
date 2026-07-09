# Use an official lightweight Python runtime
FROM python:3.11-slim

# Set system environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV WORKDIR=/workspace
# Ensure Python looks at both the workspace root and app subfolders smoothly
ENV PYTHONPATH=/workspace:/workspace/app

WORKDIR $WORKDIR

# Install system dependencies needed for Postgres and compiling C-based packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependency contracts
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the rest of your core enterprise application engine source files
COPY . .

# Expose the API engine performance gateway port
EXPOSE 8000

# Run the system using your active runtime engine startup file
# (If your FastAPI instance is defined as 'app' inside 'start_engine.py')
CMD ["uvicorn", "start_engine:app", "--host", "0.0.0.0", "--port", "8000"]
