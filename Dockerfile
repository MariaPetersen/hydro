# Use a lightweight Python base image for Raspberry Pi (ARMv7/ARM64)
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3-dev \
    gcc \
    libffi-dev \
    libjpeg-dev \
    libz-dev \
    && rm -rf /var/lib/apt/lists/*

# Create a working directory
WORKDIR /app

# Copy app files
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Export environment variable so Flask runs on 0.0.0.0
ENV FLASK_APP=pump_web.py

# Expose the Flask port
EXPOSE 5000

# Run the app
CMD ["python", "pump_web.py"]
