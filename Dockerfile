```dockerfile
FROM python:3.10-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        git \
        curl \
        wget \
        bash \
        ffmpeg \
        neofetch \
        software-properties-common && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip wheel && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "flask run -h 0.0.0.0 -p 8000 & python3 -m devgagan"]
```
