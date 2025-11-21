# 📖 Voice Authentication API - Índice de Documentação

Bem-vindo ao projeto de **Autenticação por Voz**! Este índice vai te ajudar a navegar pela documentação.

---

## 🚀 Para Começar

### Você quer...

#### **Rodar o projeto rapidamente?**
→ Leia: [`QUICKSTART.md`](QUICKSTART.md)  
⏱️ Tempo estimado: 5 minutos

#### **Entender o que é o projeto?**
→ Leia: [`SUMMARY.md`](SUMMARY.md)  
⏱️ Tempo estimado: 5 minutos

#### **Ver exemplos de código?**
→ Leia: [`EXAMPLES.md`](EXAMPLES.md)  
⏱️ Tempo estimado: 10 minutos

---

## 📚 Documentação Completa

### [`README.md`](README.md)
**Documentação principal e completa**
- Descrição do projeto
- Arquitetura
- Como executar (Docker e local)
- Endpoints da API
- Fluxo de uso
- Configuração
- Troubleshooting
- Instruções detalhadas

📖 **Quando ler**: Para entender completamente o projeto

---

### [`QUICKSTART.md`](QUICKSTART.md)
**Guia rápido de início**
- Setup em 3 passos (Docker)
- Setup local (Python)
- Primeiro teste da API
- Problemas comuns
- Links úteis

🚀 **Quando ler**: Quando você quer começar agora!

---

### [`SUMMARY.md`](SUMMARY.md)
**Resumo executivo**
- Visão geral do projeto
- Stack técnica
- Diagramas de arquitetura
- Endpoints resumidos
- Casos de uso
- Métricas de performance
- Roadmap

📊 **Quando ler**: Para apresentar o projeto a outros ou ter uma visão geral

---

### [`EXAMPLES.md`](EXAMPLES.md)
**Exemplos práticos de uso**
- Requisições com curl
- Requisições com PowerShell
- Script Python completo
- Script JavaScript/Node.js
- Como gravar áudio
- Como testar endpoints
- Queries no banco de dados

💻 **Quando ler**: Quando você quer ver código funcionando

---

### [`PROJECT_STRUCTURE.md`](PROJECT_STRUCTURE.md)
**Arquitetura e organização**
- Estrutura de pastas detalhada
- Fluxo de dados
- Modelo de dados
- Padrão de arquitetura (camadas)
- Dependências
- Logs e debugging
- Performance

🏗️ **Quando ler**: Para entender a arquitetura e contribuir com código

---

### [`DEPLOYMENT.md`](DEPLOYMENT.md)
**Guia de deploy em produção**
- Checklist pré-deploy
- Docker Compose para produção
- Nginx configuração
- Deploy em AWS, GCP, Azure
- CI/CD com GitHub Actions
- Monitoramento (Prometheus/Grafana)
- Backup e escalabilidade

🌐 **Quando ler**: Quando você quer colocar em produção

---

## 🛠️ Arquivos de Configuração

### [`docker-compose.yml`](docker-compose.yml)
Orquestração de containers (desenvolvimento)
- Serviço MySQL
- Serviço da aplicação FastAPI
- Networks e volumes

### [`Dockerfile`](Dockerfile)
Imagem Docker da aplicação
- Base Python 3.10
- Instalação de dependências
- Download de modelo Vosk
- Configuração do container

### [`requirements.txt`](requirements.txt)
Dependências Python
- FastAPI, Uvicorn, Gunicorn
- SQLAlchemy, PyMySQL
- SpeechBrain, Vosk, PyTorch
- Outras bibliotecas

### [`.env.example`](.env.example)
Exemplo de variáveis de ambiente
- Configuração do banco
- Configuração da aplicação
- Parâmetros de voz

### [`phrases.txt`](phrases.txt)
Frases de desafio para autenticação
- Lista de frases em português
- Facilmente customizável

### [`schema.sql`](schema.sql)
Schema do banco de dados MySQL
- Criação da tabela user_voice_profile
- Índices e constraints

---

## 🧪 Scripts Utilitários

### [`run_local.py`](run_local.py)
Script para executar localmente
- Verifica pré-requisitos
- Configura ambiente
- Inicia servidor

### [`test_api.py`](test_api.py)
Script de teste automatizado
- Testa health check
- Testa enrollment
- Testa verificação
- Exemplos interativos

### [`Makefile`](Makefile)
Comandos úteis do projeto
- `make install` - Instala dependências
- `make run` - Executa servidor
- `make docker-up` - Inicia containers
- `make clean` - Limpa arquivos temporários

---

## 📂 Código Fonte

### [`app/main.py`](app/main.py)
Aplicação FastAPI principal
- Configuração do app
- Middleware (CORS)
- Inclusão de routers
- Lifecycle management

### [`app/config.py`](app/config.py)
Configurações da aplicação
- Variáveis de ambiente
- Settings com Pydantic
- Database URL

### [`app/database.py`](app/database.py)
Configuração do banco de dados
- Engine SQLAlchemy
- Session management
- Dependency injection

### [`app/routers/voice.py`](app/routers/voice.py)
Rotas da API de voz
- GET /voice/challenge
- POST /voice/enroll
- POST /voice/verify

### [`app/services/voice_service.py`](app/services/voice_service.py)
Lógica de negócio
- Enrollment de usuário
- Verificação de identidade
- Gerenciamento de frases

### [`app/repositories/voice_repository.py`](app/repositories/voice_repository.py)
Acesso a dados
- CRUD de perfis de voz
- Queries no banco

### [`app/models/user_voice_profile.py`](app/models/user_voice_profile.py)
Model SQLAlchemy
- Definição da tabela
- Campos e tipos

### [`app/utils/audio_processing.py`](app/utils/audio_processing.py)
Processamento de áudio
- Transcrição com Vosk
- Extração de embedding com SpeechBrain
- Validação de transcrição

### [`app/utils/similarity.py`](app/utils/similarity.py)
Cálculo de similaridade
- Similaridade de cosseno
- Normalização de embeddings

---

## 🗺️ Roadmap de Leitura Recomendado

### **Para Desenvolvedores Iniciantes**
1. [`SUMMARY.md`](SUMMARY.md) - Entender o que é
2. [`QUICKSTART.md`](QUICKSTART.md) - Rodar rapidamente
3. [`EXAMPLES.md`](EXAMPLES.md) - Ver exemplos
4. [`README.md`](README.md) - Documentação completa

### **Para Desenvolvedores Experientes**
1. [`SUMMARY.md`](SUMMARY.md) - Visão geral
2. [`PROJECT_STRUCTURE.md`](PROJECT_STRUCTURE.md) - Arquitetura
3. Explorar código fonte em `app/`
4. [`DEPLOYMENT.md`](DEPLOYMENT.md) - Se for fazer deploy

### **Para DevOps/SRE**
1. [`SUMMARY.md`](SUMMARY.md) - Overview técnico
2. [`DEPLOYMENT.md`](DEPLOYMENT.md) - Deploy e infraestrutura
3. `docker-compose.yml` e `Dockerfile` - Containers
4. [`PROJECT_STRUCTURE.md`](PROJECT_STRUCTURE.md) - Monitoramento

### **Para Product Managers**
1. [`SUMMARY.md`](SUMMARY.md) - Visão geral e casos de uso
2. [`README.md`](README.md) - Funcionalidades detalhadas
3. Roadmap em [`SUMMARY.md`](SUMMARY.md)

---

## 🔍 Busca Rápida

### Precisa de...

**Rodar o projeto?**  
→ [`QUICKSTART.md`](QUICKSTART.md)

**Exemplos de código?**  
→ [`EXAMPLES.md`](EXAMPLES.md)

**Documentação da API?**  
→ [`README.md`](README.md) ou http://localhost:8000/docs

**Entender a arquitetura?**  
→ [`PROJECT_STRUCTURE.md`](PROJECT_STRUCTURE.md)

**Deploy em produção?**  
→ [`DEPLOYMENT.md`](DEPLOYMENT.md)

**Configurar variáveis?**  
→ [`.env.example`](.env.example)

**Ver o banco de dados?**  
→ [`schema.sql`](schema.sql)

**Testar a API?**  
→ [`test_api.py`](test_api.py)

---

## 📞 Precisa de Ajuda?

1. **Verifique os logs**: `docker-compose logs -f app`
2. **Consulte troubleshooting**: [`README.md`](README.md) seção "Troubleshooting"
3. **Veja exemplos**: [`EXAMPLES.md`](EXAMPLES.md)
4. **Abra uma issue**: GitHub Issues

---

## 🎯 Próximos Passos

Depois de explorar a documentação:

1. ✅ Execute o projeto com [`QUICKSTART.md`](QUICKSTART.md)
2. ✅ Teste os endpoints com [`EXAMPLES.md`](EXAMPLES.md)
3. ✅ Explore o código em `app/`
4. ✅ Customize para seu caso de uso
5. ✅ Deploy em produção com [`DEPLOYMENT.md`](DEPLOYMENT.md)

---

**Boa leitura e bom desenvolvimento! 🚀**

---

_Última atualização: 11 de novembro de 2025_
