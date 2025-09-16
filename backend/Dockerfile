# Use slim Python base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# System deps (psycopg2 needs libpq, shapely needs geos)
RUN apt-get update && apt-get install -y \
    libpq-dev gcc g++ \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Run app with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]