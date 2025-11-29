# Use an official lightweight Python image
FROM python:3.10-slim

# Prevent Python from writing pyc files to disc and buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies (needed for some python libraries)
RUN apt-get update && apt-get install -y --no-install-recommends gcc && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy the requirements file first (to cache dependencies)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the ports we need (8000 for API, 8501 for UI)
EXPOSE 8000
EXPOSE 8501

# By default, this image doesn't run a command. 
# We will define the commands in docker-compose.yml