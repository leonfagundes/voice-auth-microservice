# 🌐 Guia de Deploy em Produção

## 📋 Checklist Pré-Deploy

### Segurança
- [ ] Configurar autenticação nos endpoints (JWT, OAuth2)
- [ ] Habilitar HTTPS/TLS
- [ ] Configurar CORS apropriadamente
- [ ] Implementar rate limiting
- [ ] Usar secrets manager (não hard-code credenciais)
- [ ] Configurar firewall
- [ ] Sanitizar inputs
- [ ] Implementar logging de auditoria

### Performance
- [ ] Configurar cache (Redis)
- [ ] Otimizar pool de conexões do banco
- [ ] Configurar CDN (se necessário)
- [ ] Habilitar compressão de respostas
- [ ] Configurar workers Uvicorn
- [ ] Considerar uso de GPU para ML

### Monitoramento
- [ ] Configurar monitoramento de aplicação (Prometheus, Grafana)
- [ ] Configurar alertas
- [ ] Implementar health checks robustos
- [ ] Configurar logging centralizado
- [ ] Monitorar métricas de ML (acurácia, latência)

### Backup
- [ ] Configurar backup automático do banco
- [ ] Testar restore de backup
- [ ] Documentar procedimentos de recuperação

---

## 🐳 Deploy com Docker (Produção)

### 1. Docker Compose para Produção

Crie `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  db:
    image: mysql:8.0
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: ${DB_ROOT_PASSWORD}
      MYSQL_DATABASE: ${DB_NAME}
      MYSQL_USER: ${DB_USER}
      MYSQL_PASSWORD: ${DB_PASSWORD}
    volumes:
      - mysql_data:/var/lib/mysql
      - ./backups:/backups
    networks:
      - auth_voice_network
    # Não expor porta publicamente em produção
    # Use apenas para acesso interno

  app:
    build:
      context: .
      dockerfile: Dockerfile.prod
    restart: always
    ports:
      - "8000:8000"
    environment:
      DB_HOST: db
      DB_PORT: 3306
      DB_USER: ${DB_USER}
      DB_PASSWORD: ${DB_PASSWORD}
      DB_NAME: ${DB_NAME}
      DEBUG: "False"
      SIMILARITY_THRESHOLD: ${SIMILARITY_THRESHOLD:-0.75}
    depends_on:
      db:
        condition: service_healthy
    networks:
      - auth_voice_network
    # Limitar recursos
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
        reservations:
          cpus: '1'
          memory: 2G

  nginx:
    image: nginx:alpine
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - app
    networks:
      - auth_voice_network

volumes:
  mysql_data:

networks:
  auth_voice_network:
    driver: bridge
```

### 2. Dockerfile para Produção

`Dockerfile.prod`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc g++ wget curl git \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Baixar modelo Vosk
RUN mkdir -p models && \
    cd models && \
    wget https://alphacephei.com/vosk/models/vosk-model-small-pt-0.3.zip && \
    unzip vosk-model-small-pt-0.3.zip && \
    rm vosk-model-small-pt-0.3.zip

# Copiar código
COPY ./app /app/app
COPY phrases.txt /app/phrases.txt

# Criar usuário não-root
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000

# Usar Gunicorn com Uvicorn workers para produção
CMD ["gunicorn", "app.main:app", \
     "--workers", "4", \
     "--worker-class", "uvicorn.workers.UvicornWorker", \
     "--bind", "0.0.0.0:8000", \
     "--timeout", "120", \
     "--access-logfile", "-", \
     "--error-logfile", "-"]
```

### 3. Nginx Configuration

`nginx.conf`:

```nginx
events {
    worker_connections 1024;
}

http {
    upstream app {
        server app:8000;
    }

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;

    server {
        listen 80;
        server_name your-domain.com;
        
        # Redirect to HTTPS
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl http2;
        server_name your-domain.com;

        # SSL Configuration
        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers HIGH:!aNULL:!MD5;

        # Client body size limit (para uploads de áudio)
        client_max_body_size 10M;

        # Apply rate limiting
        limit_req zone=api_limit burst=20 nodelay;

        location / {
            proxy_pass http://app;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            
            # Timeouts
            proxy_connect_timeout 60s;
            proxy_send_timeout 60s;
            proxy_read_timeout 60s;
        }

        # Healthcheck endpoint (não aplicar rate limit)
        location /health {
            limit_req off;
            proxy_pass http://app/health;
        }
    }
}
```

---

## ☁️ Deploy em Cloud

### AWS (Elastic Beanstalk)

1. **Instalar EB CLI**
```bash
pip install awsebcli
```

2. **Inicializar**
```bash
eb init -p docker voice-auth-api
```

3. **Criar ambiente**
```bash
eb create voice-auth-prod
```

4. **Deploy**
```bash
eb deploy
```

### Google Cloud (Cloud Run)

1. **Build imagem**
```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/voice-auth
```

2. **Deploy**
```bash
gcloud run deploy voice-auth \
  --image gcr.io/PROJECT_ID/voice-auth \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Azure (Container Instances)

1. **Login**
```bash
az login
```

2. **Criar grupo de recursos**
```bash
az group create --name voice-auth-rg --location eastus
```

3. **Deploy container**
```bash
az container create \
  --resource-group voice-auth-rg \
  --name voice-auth-app \
  --image your-registry/voice-auth:latest \
  --dns-name-label voice-auth \
  --ports 8000
```

---

## 🔐 Variáveis de Ambiente (Produção)

Crie arquivo `.env.prod`:

```env
# Database
DB_HOST=your-db-host
DB_PORT=3306
DB_USER=production_user
DB_PASSWORD=STRONG_PASSWORD_HERE
DB_NAME=auth_voice_db

# Application
APP_HOST=0.0.0.0
APP_PORT=8000
DEBUG=False

# Security
SECRET_KEY=YOUR_SECRET_KEY_HERE
ALLOWED_HOSTS=your-domain.com,www.your-domain.com

# Voice Authentication
SIMILARITY_THRESHOLD=0.75
VOSK_MODEL_PATH=./models/vosk-model-small-pt-0.3
SPEECHBRAIN_MODEL=speechbrain/spkrec-ecapa-voxceleb

# Logging
LOG_LEVEL=INFO
```

---

## 📊 Monitoramento

### Prometheus + Grafana

1. **Adicionar ao docker-compose.prod.yml**:

```yaml
  prometheus:
    image: prom/prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    ports:
      - "9090:9090"
    networks:
      - auth_voice_network

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    volumes:
      - grafana_data:/var/lib/grafana
    networks:
      - auth_voice_network
```

2. **Instalar biblioteca de métricas**:
```bash
pip install prometheus-fastapi-instrumentator
```

3. **Adicionar ao main.py**:
```python
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(...)

Instrumentator().instrument(app).expose(app)
```

---

## 🔄 CI/CD

### GitHub Actions

`.github/workflows/deploy.yml`:

```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Build Docker image
      run: docker build -t voice-auth:latest .
    
    - name: Run tests
      run: docker run voice-auth:latest pytest
    
    - name: Push to registry
      run: |
        echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
        docker tag voice-auth:latest ${{ secrets.DOCKER_USERNAME }}/voice-auth:latest
        docker push ${{ secrets.DOCKER_USERNAME }}/voice-auth:latest
    
    - name: Deploy to server
      uses: appleboy/ssh-action@master
      with:
        host: ${{ secrets.HOST }}
        username: ${{ secrets.USERNAME }}
        key: ${{ secrets.SSH_KEY }}
        script: |
          cd /app/voice-auth
          docker-compose pull
          docker-compose up -d
```

---

## 📈 Escalabilidade

### Horizontal Scaling

1. **Load Balancer**
   - Use Nginx, HAProxy ou cloud load balancer

2. **Multiple Instances**
   ```bash
   docker-compose up -d --scale app=3
   ```

3. **Database Replication**
   - Configure MySQL master-slave
   - Use read replicas

### Cache Layer

Adicione Redis:

```yaml
  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
```

---

## 🛡️ Backup

### Script de Backup Automático

`backup.sh`:

```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups"

# Backup do banco de dados
docker exec auth_voice_mysql mysqldump \
  -u root -p$MYSQL_ROOT_PASSWORD \
  auth_voice_db > $BACKUP_DIR/db_backup_$DATE.sql

# Compactar
gzip $BACKUP_DIR/db_backup_$DATE.sql

# Manter apenas últimos 7 dias
find $BACKUP_DIR -name "db_backup_*.sql.gz" -mtime +7 -delete
```

Agendar com cron:
```bash
0 2 * * * /path/to/backup.sh
```

---

## 📞 Suporte e Manutenção

- Monitore logs regularmente
- Mantenha dependências atualizadas
- Aplique patches de segurança
- Realize testes de carga periódicos
- Documente mudanças

---

**Boa sorte com o deploy! 🚀**
