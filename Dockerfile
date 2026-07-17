FROM python:3.11-slim

# Install system dependencies for Pillow/OpenCV
RUN apt-get update && apt-get install -y \
    libjpeg-dev \
    zlib1g-dev \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt

# Copy application files
COPY . .

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "run:app"]
