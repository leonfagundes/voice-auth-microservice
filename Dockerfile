FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    wget \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p models && \
    cd models && \
    wget https://alphacephei.com/vosk/models/vosk-model-small-pt-0.3.zip && \
    unzip vosk-model-small-pt-0.3.zip && \
    rm vosk-model-small-pt-0.3.zip

COPY ./app /app/app
COPY phrases.txt /app/phrases.txt
COPY .env.example /app/.env

RUN mkdir -p /app/models/speechbrain

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
