# Use a slim base image for Python 3.10 on Debian Buster
FROM python:3.10-slim-buster

# Set the working directory inside the container
WORKDIR /app

# Copy only the requirements file first to leverage Docker's build cache
# If requirements.txt doesn't change, this layer can be cached, speeding up rebuilds
COPY docker_requirements.txt .

# Install Python dependencies
# Combine apt-get update and pip install into a single RUN command
# to reduce the number of layers and improve build cache efficiency.
RUN apt-get update && \
    pip install --no-cache-dir -r docker_requirements.txt && \
    rm -rf /var/lib/apt/lists/*

# Install AzCopy
# This is a multi-step process:
# 1. Install curl and gnupg (needed for adding external apt repositories)
# 2. Download and add the Microsoft GPG key
# 3. Add the Microsoft package repository to your sources list
#    - For Debian Buster (Debian 10), the distribution is 'debian' and version is '10/prod'.
#    - Specify 'amd64' architecture if your base image is amd64.
# 4. Update apt-get again to recognize the new repository
# 5. Install azcopy
# 6. Clean up apt cache and temporary files to keep the image size small
RUN apt-get update && \
    apt-get install -y curl gnupg && \
    curl -sL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > /etc/apt/trusted.gpg.d/microsoft.gpg && \
    echo "deb [arch=amd64] https://packages.microsoft.com/debian/10/prod buster main" > /etc/apt/sources.list.d/microsoft.list && \
    apt-get update && \
    apt-get install -y azcopy && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Copy the rest of your application code into the container
# This step runs after dependencies are installed, so changes to code don't invalidate
# the dependency layers, again improving build times.
COPY . /app

# Command to run your application when the container starts
CMD ["python3", "app.py"]