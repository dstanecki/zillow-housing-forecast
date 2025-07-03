# Use the official Python image from Docker Hub
FROM python:3.8-slim

# Set the working directory inside the container
WORKDIR /app

# Install build dependencies and MariaDB dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    mariadb-client \
    libmariadb-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Install Prometheus exporter 
RUN pip install prometheus_flask_exporter

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port that the Flask app runs on
EXPOSE 5000

# Command to run the Flask application
CMD ["python", "application.py"]
