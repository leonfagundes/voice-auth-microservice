# 🎙️ Voice Authentication API - Estrutura do Projeto

## 📁 Estrutura de Arquivos

```
auth-voice/
│
├── app/                                # Código principal da aplicação
│   ├── __init__.py
│   ├── main.py                         # Aplicação FastAPI principal
│   ├── config.py                       # Configurações e variáveis de ambiente
│   ├── database.py                     # Configuração SQLAlchemy e sessões
│   │
│   ├── models/                         # Models do banco de dados
│   │   ├── __init__.py
│   │   └── user_voice_profile.py      # Model de perfil de voz
│   │
│   ├── repositories/                   # Camada de acesso a dados
│   │   ├── __init__.py
│   │   └── voice_repository.py        # Repository para operações no BD
│   │
│   ├── services/                       # Lógica de negócio
│   │   ├── __init__.py
│   │   └── voice_service.py           # Serviço de autenticação por voz
│   │
│   ├── routers/                        # Rotas da API
│   │   ├── __init__.py
│   │   └── voice.py                   # Endpoints de voz
│   │
│   └── utils/                          # Utilitários
│       ├── __init__.py
│       ├── audio_processing.py        # Processamento de áudio (Vosk + SpeechBrain)
│       └── similarity.py              # Cálculo de similaridade
│
├── docs/                               # Documentação
│   ├── README.md                       # Índice da documentação
│   ├── QUICKSTART.md
│   ├── GUIA_USO.md
│   ├── TESTES_SEM_APP.md
│   ├── PROJECT_STRUCTURE.md            # Este arquivo
│   ├── DEPLOYMENT.md
│   ├── EXAMPLES.md
│   ├── AUDITORIA_CODIGO.md
│   ├── CHECKLIST.md
│   ├── STATUS_ATUAL.md
│   ├── DEPENDENCIES_STATUS.md
│   ├── MODELO_INSTALADO.md
│   ├── INDEX.md
│   ├── SUMMARY.md
│   └── EXPO_SETUP_GUIDE.txt
│
├── scripts/                            # Scripts utilitários
│   ├── README.md                       # Documentação dos scripts
│   ├── start_api.py                    # Iniciar API
│   ├── run_local.py
│   ├── teste_rapido.py
│   ├── test_completo.py
│   ├── gravar_audio.py
│   ├── test_api.py
│   ├── test_db_connection.py
│   ├── test_embeddings_final.py
│   ├── test_simple_api.py
│   ├── test_speechbrain_api.py
│   ├── download_vosk_model.py
│   ├── fix_speechbrain_symlink.py
│   └── copy_all_speechbrain_files.py
│
├── models/                             # Modelos de ML (criado em runtime)
│   ├── vosk-model-small-pt-0.3/       # Modelo Vosk (baixado)
│   └── speechbrain/                    # Cache do SpeechBrain
│
├── .env.example                        # Exemplo de variáveis de ambiente
├── .env                                # Configurações locais (não versionado)
├── .gitignore                          # Arquivos ignorados pelo Git
├── .dockerignore                       # Arquivos ignorados pelo Docker
│
├── Dockerfile                          # Configuração da imagem Docker
├── docker-compose.yml                  # Orquestração de containers
│
├── requirements.txt                    # Dependências Python
├── phrases.txt                         # Frases para desafio de voz
├── schema.sql                          # Schema do banco (referência)
├── Makefile                            # Comandos úteis
├── expo-api-config.js                  # Configuração para Expo
├── Voice_Auth_API.postman_collection.json
│
└── README.md                           # Documentação principal
```

## 🔄 Fluxo de Dados

### Enrollment (Cadastro)
```
Cliente
  │
  ├─► GET /voice/challenge
  │     └─► VoiceService.get_challenge_phrase()
  │           └─► Retorna frase aleatória
  │
  └─► POST /voice/enroll
        ├─► Recebe: user_id, audio_file, phrase_expected
        ├─► VoiceService.enroll_user()
        │     ├─► audio_processing.transcribe_audio() [Vosk]
        │     ├─► audio_processing.validate_transcription()
        │     ├─► audio_processing.extract_voice_embedding() [SpeechBrain]
        │     └─► VoiceRepository.create_profile()
        │           └─► Salva embedding no MySQL
        └─► Retorna: success, message, transcription
```

### Verificação (Autenticação)
```
Cliente
  │
  ├─► GET /voice/challenge
  │     └─► Obtém frase para pronunciar
  │
  └─► POST /voice/verify
        ├─► Recebe: user_id, audio_file, phrase_expected
        ├─► VoiceService.verify_user()
        │     ├─► VoiceRepository.get_profile_by_user_id()
        │     │     └─► Busca embedding armazenado
        │     ├─► audio_processing.transcribe_audio() [Vosk]
        │     ├─► audio_processing.validate_transcription()
        │     ├─► audio_processing.extract_voice_embedding() [SpeechBrain]
        │     └─► similarity.calculate_cosine_similarity()
        │           └─► Compara embeddings
        └─► Retorna: authenticated, similarity, message
```

## 🗄️ Modelo de Dados

### Tabela: user_voice_profile

| Campo      | Tipo         | Descrição                              |
|------------|--------------|----------------------------------------|
| id         | INT          | Chave primária (auto increment)        |
| user_id    | VARCHAR(255) | ID único do usuário (unique, indexed)  |
| embedding  | JSON         | Vetor de características vocais        |
| created_at | TIMESTAMP    | Data de criação do registro            |
| updated_at | TIMESTAMP    | Data da última atualização             |

### Estrutura do Embedding
```json
{
  "embedding": [0.123, -0.456, 0.789, ..., 0.234]  // Array de ~192 dimensões
}
```

## 🏗️ Padrão de Arquitetura

O projeto segue uma **arquitetura em camadas**:

1. **Routers** (`app/routers/`)
   - Recebem requisições HTTP
   - Validam entrada
   - Delegam para Services

2. **Services** (`app/services/`)
   - Contêm lógica de negócio
   - Orquestram operações
   - Usam Repositories e Utils

3. **Repositories** (`app/repositories/`)
   - Abstraem acesso ao banco
   - Operações CRUD
   - Isolam SQLAlchemy

4. **Models** (`app/models/`)
   - Definem estrutura do banco
   - Mapeamento ORM

5. **Utils** (`app/utils/`)
   - Funções auxiliares
   - Processamento de áudio
   - Cálculos matemáticos

## 🔧 Configuração

### Variáveis de Ambiente (.env)
```env
# Banco de Dados
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=rootpassword
DB_NAME=auth_voice_db

# Aplicação
APP_HOST=0.0.0.0
APP_PORT=8000
DEBUG=True

# Autenticação por Voz
SIMILARITY_THRESHOLD=0.75                           # Limiar de similaridade (0-1)
VOSK_MODEL_PATH=./models/vosk-model-small-pt-0.3   # Caminho do modelo Vosk
SPEECHBRAIN_MODEL=speechbrain/spkrec-ecapa-voxceleb # Modelo SpeechBrain
```

## 🐳 Docker

### Serviços no docker-compose.yml

1. **db** (MySQL 8.0)
   - Porta: 3306
   - Volume: mysql_data
   - Healthcheck configurado

2. **app** (FastAPI)
   - Porta: 8000
   - Depende de: db
   - Volumes montados para desenvolvimento

## 📚 Dependências Principais

### Framework Web
- **FastAPI**: Framework web moderno e rápido
- **Uvicorn**: ASGI server
- **Pydantic**: Validação de dados

### Banco de Dados
- **SQLAlchemy**: ORM
- **PyMySQL**: Driver MySQL

### Machine Learning / IA
- **SpeechBrain**: Extração de embeddings vocais
- **Vosk**: Reconhecimento de fala (ASR)
- **PyTorch**: Framework de deep learning
- **Torchaudio**: Processamento de áudio

### Utilidades
- **NumPy**: Computação numérica
- **scikit-learn**: Cálculo de similaridade
- **python-dotenv**: Gerenciamento de variáveis de ambiente

## 🚀 Comandos Úteis

### Com Docker
```bash
# Iniciar
docker-compose up --build

# Parar
docker-compose down

# Ver logs
docker-compose logs -f app

# Acessar MySQL
docker exec -it auth_voice_mysql mysql -uroot -prootpassword auth_voice_db
```

### Sem Docker (Local)
```bash
# Setup
python -m venv venv
.\venv\Scripts\activate  # Windows
pip install -r requirements.txt

# Executar
python run_local.py

# OU
uvicorn app.main:app --reload

# Testar
python test_api.py
```

## 📊 Logs

Os logs seguem o formato:
```
YYYY-MM-DD HH:MM:SS - module_name - LEVEL - message
```

Exemplo:
```
2025-11-11 10:30:45 - app.services.voice_service - INFO - Enrollment concluído para usuário user123
```

## 🔐 Segurança (Produção)

Para uso em produção, considere:

- [ ] Autenticação/autorização nos endpoints (JWT, OAuth2)
- [ ] HTTPS/TLS
- [ ] CORS apropriado
- [ ] Rate limiting
- [ ] Validação rigorosa de inputs
- [ ] Sanitização de dados
- [ ] Secrets management
- [ ] Auditoria e monitoring
- [ ] Backup do banco de dados
- [ ] Limites de tamanho de upload

## 📈 Performance

### Otimizações Implementadas
- ✅ Cache de modelos ML (singleton)
- ✅ Connection pooling no banco
- ✅ Índices no banco de dados
- ✅ Processamento assíncrono (FastAPI)

### Melhorias Futuras
- [ ] Cache Redis para embeddings
- [ ] Fila de processamento (Celery)
- [ ] CDN para arquivos estáticos
- [ ] GPU para inferência ML
- [ ] Compressão de embeddings

## 🧪 Testes

### Estrutura de Testes (a implementar)
```
tests/
├── test_audio_processing.py
├── test_similarity.py
├── test_voice_service.py
├── test_voice_repository.py
└── test_endpoints.py
```

### Executar testes (quando implementados)
```bash
pytest tests/ -v
pytest tests/ --cov=app
```

## 📝 Licença

Este projeto é fornecido como exemplo educacional.

---

**Última atualização:** 11 de novembro de 2025
