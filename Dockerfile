FROM python:3.10-slim-buster

WORKDIR /app

COPY docker_requirements.txt .

RUN apt-get update && \
    pip install --no-cache-dir -r docker_requirements.txt && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update && \
    apt-get install -y curl gnupg && \
    curl -sL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > /etc/apt/trusted.gpg.d/microsoft.gpg && \
    echo "deb [arch=amd64] https://packages.microsoft.com/debian/10/prod buster main" > /etc/apt/sources.list.d/microsoft.list && \
    apt-get update && \
    apt-get install -y azcopy && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY . /app

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
