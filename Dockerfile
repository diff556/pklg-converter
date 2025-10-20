# Start from an official Python image
FROM python:3.9-slim

# This line prevents apt-get from asking interactive questions during build
ENV DEBIAN_FRONTEND=noninteractive

# Install the FULL wireshark suite to ensure all dissectors are present
RUN apt-get update && apt-get install -y wireshark

# Set up the working directory
WORKDIR /app

# Copy the requirements file and install Python libraries
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Run as a non-root user for better security and compatibility
RUN useradd --create-home appuser
USER appuser

# Tell Render that the service will be listening on this port
EXPOSE 10000

# Command to run the web server
CMD ["/usr/local/bin/gunicorn", "--workers", "1", "--bind", "0.0.0.0:10000", "app:app"]