# Start from an official Python image
FROM python:3.9-slim

# Install tshark and its dependencies
RUN apt-get update && apt-get install -y tshark

# Set up the working directory
WORKDIR /app

# Copy the requirements file and install Python libraries
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Command to run the web server
CMD gunicorn --bind 0.0.0.0:$PORT app:app