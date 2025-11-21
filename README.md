# Voice Authentication API

API de autenticação por voz usando **FastAPI**, **SpeechBrain** e **Vosk** para reconhecimento e verificação de locutor.

> 📚 **Documentação Completa**: [docs/README.md](docs/README.md)  
> 🔌 **API Reference**: [docs/API_REFERENCE.md](docs/API_REFERENCE.md)  
> 🚀 **Quick Start**: [docs/QUICKSTART.md](docs/QUICKSTART.md)  
> 📱 **App Exemplo**: [voice-auth-app](https://github.com/leonfagundes/voice-auth-app)

## 📋 Descrição

Microsserviço completo de autenticação biométrica por voz que permite:
1. **Enrollment** (cadastro de perfil de voz)
2. **Verificação** de identidade através da voz
3. Validação de texto pronunciado (anti-replay)

### Características
- ✅ Não armazena áudio bruto, apenas embeddings vetoriais
- ✅ Validação de transcrição usando Vosk
- ✅ Extração de características vocais com SpeechBrain
- ✅ Similaridade por cosseno para verificação
- ✅ Threshold configurável (padrão: 0.75)
- ✅ MySQL para persistência
- ✅ Docker + Docker Compose

## 🏗️ Arquitetura

```
auth-voice/
├── app/
│   ├── main.py                 # Aplicação FastAPI
│   ├── config.py               # Configurações
│   ├── database.py             # Setup do SQLAlchemy
│   ├── models/
│   │   └── user_voice_profile.py
│   ├── repositories/
│   │   └── voice_repository.py
│   ├── services/
│   │   └── voice_service.py
│   ├── routers/
│   │   └── voice.py           # Endpoints da API
│   └── utils/
│       ├── audio_processing.py # Vosk + SpeechBrain
│       └── similarity.py       # Cálculo de similaridade
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── phrases.txt                # Frases de desafio
└── README.md
```

## 🚀 Como Executar

### Pré-requisitos
- Docker
- Docker Compose

### Passo 1: Clonar o repositório
```bash
git clone <repo-url>
cd auth-voice
```

### Passo 2: Configurar variáveis de ambiente (opcional)
Copie o arquivo `.env.example` para `.env` e ajuste se necessário:
```bash
cp .env.example .env
```

### Passo 3: Executar com Docker Compose
```bash
docker-compose up --build
```

A API estará disponível em: `http://localhost:8000`

### Passo 4: Acessar documentação
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 📡 Endpoints

### 1. GET /voice/challenge
Retorna uma frase aleatória para o usuário pronunciar.

**Response:**
```json
{
  "phrase": "Minha voz é minha identidade"
}
```

**Exemplo com curl:**
```bash
curl http://localhost:8000/voice/challenge
```

**Exemplo com httpie:**
```bash
http GET http://localhost:8000/voice/challenge
```

---

### 2. POST /voice/enroll
Cadastra o perfil de voz de um usuário.

**Parâmetros (multipart/form-data):**
- `user_id`: ID único do usuário (string)
- `phrase_expected`: Frase esperada (string)
- `audio_file`: Arquivo de áudio WAV (file)

**Response (sucesso):**
```json
{
  "success": true,
  "message": "Perfil de voz cadastrado com sucesso",
  "user_id": "user123",
  "transcription": "minha voz é minha identidade"
}
```

**Exemplo com curl:**
```bash
curl -X POST http://localhost:8000/voice/enroll \
  -F "user_id=user123" \
  -F "phrase_expected=Minha voz é minha identidade" \
  -F "audio_file=@audio.wav"
```

**Exemplo com httpie:**
```bash
http -f POST http://localhost:8000/voice/enroll \
  user_id="user123" \
  phrase_expected="Minha voz é minha identidade" \
  audio_file@audio.wav
```

---

### 3. POST /voice/verify
Verifica a identidade de um usuário através da voz.

**Parâmetros (multipart/form-data):**
- `user_id`: ID único do usuário (string)
- `phrase_expected`: Frase esperada (string)
- `audio_file`: Arquivo de áudio WAV (file)

**Response (autenticado):**
```json
{
  "authenticated": true,
  "similarity": 0.8732,
  "threshold": 0.75,
  "message": "Autenticação bem-sucedida",
  "transcription": "minha voz é minha identidade"
}
```

**Response (não autenticado):**
```json
{
  "authenticated": false,
  "similarity": 0.5234,
  "threshold": 0.75,
  "message": "Voz não reconhecida",
  "transcription": "minha voz é minha identidade"
}
```

**Exemplo com curl:**
```bash
curl -X POST http://localhost:8000/voice/verify \
  -F "user_id=user123" \
  -F "phrase_expected=Minha voz é minha identidade" \
  -F "audio_file=@audio.wav"
```

**Exemplo com httpie:**
```bash
http -f POST http://localhost:8000/voice/verify \
  user_id="user123" \
  phrase_expected="Minha voz é minha identidade" \
  audio_file@audio.wav
```

## 🎯 Fluxo de Uso

### Enrollment (Cadastro)
1. Cliente chama `GET /voice/challenge` para obter uma frase
2. Usuário grava áudio pronunciando a frase
3. Cliente envia para `POST /voice/enroll` com user_id, frase e áudio
4. Sistema valida transcrição e armazena embedding

### Verificação (Login)
1. Cliente chama `GET /voice/challenge` para obter uma frase
2. Usuário grava áudio pronunciando a frase
3. Cliente envia para `POST /voice/verify` com user_id, frase e áudio
4. Sistema valida e retorna se autenticado ou não

## ⚙️ Configuração

### Variáveis de Ambiente (.env)
```env
# Database
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=rootpassword
DB_NAME=auth_voice_db

# Application
APP_HOST=0.0.0.0
APP_PORT=8000
DEBUG=True

# Voice Authentication
SIMILARITY_THRESHOLD=0.75
VOSK_MODEL_PATH=./models/vosk-model-small-pt-0.3
SPEECHBRAIN_MODEL=speechbrain/spkrec-ecapa-voxceleb
```

### Ajustar Threshold de Similaridade
Para tornar a autenticação mais ou menos rigorosa, ajuste `SIMILARITY_THRESHOLD`:
- **0.6 - 0.7**: Menos rigoroso (mais falsos positivos)
- **0.75**: Padrão balanceado
- **0.8 - 0.9**: Mais rigoroso (mais falsos negativos)

## 🗄️ Banco de Dados

### Tabela: user_voice_profile
| Campo      | Tipo     | Descrição                           |
|------------|----------|-------------------------------------|
| id         | INT      | Primary key (auto increment)        |
| user_id    | VARCHAR  | ID único do usuário (unique)        |
| embedding  | JSON     | Vetor de embedding da voz           |
| created_at | DATETIME | Data de criação                     |
| updated_at | DATETIME | Data de atualização                 |

## 📦 Dependências Principais

- **FastAPI**: Framework web
- **Uvicorn**: ASGI server
- **SQLAlchemy**: ORM
- **PyMySQL**: Driver MySQL
- **SpeechBrain**: Extração de embeddings vocais
- **Vosk**: Reconhecimento de fala (ASR)
- **scikit-learn**: Cálculo de similaridade

## 🧪 Testando com Áudio de Exemplo

### Criar um áudio de teste (Windows PowerShell)
Você pode gravar um áudio usando o gravador do Windows ou usar ferramentas como:
- Audacity
- Windows Voice Recorder
- ffmpeg

Certifique-se de que o formato seja WAV, mono, 16kHz (recomendado).

### Converter áudio para WAV com ffmpeg
```bash
ffmpeg -i input.mp3 -ar 16000 -ac 1 output.wav
```

## 🐛 Troubleshooting

### Modelo Vosk não encontrado
O Dockerfile baixa automaticamente o modelo português. Se precisar fazer manualmente:
```bash
mkdir -p models
cd models
wget https://alphacephei.com/vosk/models/vosk-model-small-pt-0.3.zip
unzip vosk-model-small-pt-0.3.zip
```

### Erro de conexão com MySQL
Aguarde o MySQL inicializar completamente. O docker-compose já está configurado com healthcheck.

### Baixa acurácia na transcrição
- Use áudio com boa qualidade (sem ruído)
- Fale claramente
- Use microfone de qualidade
- Formato WAV 16kHz mono é ideal

## 📝 Logs

Os logs são exibidos no console com formato:
```
2025-11-11 10:30:45 - app.services.voice_service - INFO - Enrollment concluído para usuário user123
```

## 🔒 Segurança

### Considerações de Produção
- [ ] Implementar autenticação/autorização para os endpoints
- [ ] Usar HTTPS
- [ ] Configurar CORS apropriadamente
- [ ] Limitar tamanho de upload de arquivos
- [ ] Implementar rate limiting
- [ ] Usar secrets manager para credenciais
- [ ] Adicionar sanitização de inputs
- [ ] Implementar auditoria de acessos

## 📄 Licença

Este projeto é fornecido como exemplo educacional.

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se livre para abrir issues ou pull requests.

## 📧 Contato

Para dúvidas ou sugestões, abra uma issue no repositório.

---

**Desenvolvido com ❤️ usando FastAPI, SpeechBrain e Vosk**
