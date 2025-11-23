FROM python:3.10-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    wget \
    curl \
    git \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download do modelo Vosk
RUN mkdir -p models && \
    cd models && \
    wget https://alphacephei.com/vosk/models/vosk-model-small-pt-0.3.zip && \
    unzip vosk-model-small-pt-0.3.zip && \
    rm vosk-model-small-pt-0.3.zip

# Copiar modelos SpeechBrain pré-treinados
COPY ./models/speechbrain /app/models/speechbrain

# Copiar código da aplicação
COPY ./app /app/app
COPY phrases.txt /app/phrases.txt
COPY .env.example /app/.env

# Criar diretório para arquivos temporários de áudio
RUN mkdir -p /app/temp

# Expor porta
EXPOSE 8000

# Comando de inicialização
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
