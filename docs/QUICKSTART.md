# 🚀 Guia Rápido de Início

## Opção 1: Docker (Recomendado) 🐳

### Passo 1: Pré-requisitos
- Docker Desktop instalado
- Git (opcional)

### Passo 2: Executar
```bash
# Navegue até a pasta do projeto
cd auth-voice

# Inicie os containers
docker-compose up --build
```

### Passo 3: Testar
Abra o navegador em: **http://localhost:8000/docs**

✅ **Pronto!** A API está rodando.

---

## Opção 2: Local (Desenvolvimento) 💻

### Passo 1: Pré-requisitos
- Python 3.10+
- MySQL 8.0+
- Git (opcional)

### Passo 2: Setup
```bash
# Navegue até a pasta
cd auth-voice

# Crie ambiente virtual
python -m venv venv

# Ative o ambiente (Windows)
.\venv\Scripts\activate

# Instale dependências
pip install -r requirements.txt
```

### Passo 3: Baixar Modelo Vosk
```bash
# Crie a pasta
mkdir models
cd models

# Baixe e extraia o modelo
# Windows: baixe manualmente de https://alphacephei.com/vosk/models/vosk-model-small-pt-0.3.zip
# Extraia em: models/vosk-model-small-pt-0.3/
```

### Passo 4: Configurar Banco
```bash
# Configure o MySQL (já deve estar rodando)
# Crie o banco de dados:
mysql -u root -p
```

```sql
CREATE DATABASE auth_voice_db;
```

### Passo 5: Configurar .env
```bash
# Copie o exemplo
cp .env.example .env

# Edite .env com suas configurações
# DB_HOST=localhost
# DB_USER=root
# DB_PASSWORD=sua_senha
```

### Passo 6: Executar
```bash
# Opção 1: Com script helper
python run_local.py

# Opção 2: Direto
uvicorn app.main:app --reload
```

✅ **Pronto!** Acesse http://localhost:8000/docs

---

## 📝 Primeiro Teste

### 1. Obter frase de desafio
```bash
curl http://localhost:8000/voice/challenge
```

Resposta:
```json
{
  "phrase": "Minha voz é minha identidade"
}
```

### 2. Gravar áudio
Grave um áudio de 2-3 segundos pronunciando a frase.
Salve como `test_audio.wav`

### 3. Fazer enrollment
```bash
curl -X POST http://localhost:8000/voice/enroll \
  -F "user_id=usuario_teste" \
  -F "phrase_expected=Minha voz é minha identidade" \
  -F "audio_file=@test_audio.wav"
```

### 4. Verificar identidade
```bash
curl -X POST http://localhost:8000/voice/verify \
  -F "user_id=usuario_teste" \
  -F "phrase_expected=Minha voz é minha identidade" \
  -F "audio_file=@test_audio.wav"
```

---

## 🎯 Próximos Passos

1. **Explore a documentação interativa**
   - http://localhost:8000/docs (Swagger)
   - http://localhost:8000/redoc (ReDoc)

2. **Leia os guias**
   - `README.md` - Documentação completa
   - `EXAMPLES.md` - Exemplos de código
   - `PROJECT_STRUCTURE.md` - Arquitetura

3. **Teste com script Python**
   ```bash
   python test_api.py
   ```

4. **Customize**
   - Adicione suas próprias frases em `phrases.txt`
   - Ajuste o threshold em `.env`
   - Explore os endpoints na documentação

---

## ❓ Problemas Comuns

### Porta 8000 já em uso
```bash
# Use outra porta
uvicorn app.main:app --port 8001
```

### MySQL não conecta
- Verifique se o MySQL está rodando
- Confira as credenciais no `.env`
- Teste: `mysql -u root -p`

### Modelo Vosk não encontrado
- Baixe de https://alphacephei.com/vosk/models
- Extraia em `models/vosk-model-small-pt-0.3/`
- Verifique o caminho no `.env`

### Erro ao importar bibliotecas
```bash
# Reinstale as dependências
pip install -r requirements.txt --force-reinstall
```

---

## 📞 Suporte

- Abra uma issue no GitHub
- Consulte a documentação completa
- Verifique os logs: `docker-compose logs -f app`

---

**Boa sorte! 🎉**
