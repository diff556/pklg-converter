# Start from an official Python image
FROM python:3.9-slim

# This line prevents apt-get from asking interactive questions
ENV DEBIAN_FRONTEND=noninteractive

# Install tshark and its dependencies
RUN apt-get update && apt-get install -y tshark

# Set up the working directory
WORKDIR /app

# Copy the requirements file and install Python libraries
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the port the app runs on
EXPOSE 10000

# Command to run the web server
# We use the full path to be 100% sure it's found
CMD ["/usr/local/bin/gunicorn", "--bind", "0.0.0.0:10000", "app:app"]