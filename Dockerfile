# Start from the official Debian image, which is more standard for apt
FROM debian:bullseye-slim

# Set an environment variable to ensure apt-get runs non-interactively
ENV DEBIAN_FRONTEND=noninteractive

# Update the package lists and install the full Wireshark suite and Python.
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    wireshark \
    python3 \
    python3-pip && \
    # Clean up the apt cache to keep the image smaller
    rm -rf /var/lib/apt/lists/*

# --- THIS IS THE NEW DIAGNOSTIC LINE ---
# This command will find and print the full path of the tshark executable to the build logs.
RUN which tshark
# ------------------------------------

# Set up the working directory
WORKDIR /app

# Copy the requirements file and install Python libraries
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Create and switch to a non-root user
RUN useradd --create-home appuser
USER appuser

# Expose the port the app runs on
EXPOSE 10000

# Command to run the web server, using the full path for gunicorn
CMD ["/usr/local/bin/gunicorn", "--workers", "1", "--bind", "0.0.0.0:10000", "app:app"]