# Scripts de Exemplo para Teste da API

## Testando Localmente (sem Docker)

### 1. Configurar ambiente virtual
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 2. Baixar modelo Vosk
```bash
mkdir models
cd models
# Baixe de: https://alphacephei.com/vosk/models/vosk-model-small-pt-0.3.zip
# Extraia na pasta models/
```

### 3. Configurar variáveis de ambiente
```bash
cp .env.example .env
# Edite o .env com as configurações do seu MySQL local
```

### 4. Iniciar servidor
```bash
python -m uvicorn app.main:app --reload
```

---

## Exemplos de Requisições

### PowerShell (Windows)

#### 1. Obter frase de desafio
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/voice/challenge" -Method GET
```

#### 2. Fazer enrollment
```powershell
$headers = @{}
$formData = @{
    user_id = "user123"
    phrase_expected = "Minha voz é minha identidade"
    audio_file = Get-Item -Path ".\audio.wav"
}

Invoke-RestMethod -Uri "http://localhost:8000/voice/enroll" `
    -Method POST `
    -Form $formData
```

#### 3. Verificar usuário
```powershell
$formData = @{
    user_id = "user123"
    phrase_expected = "Minha voz é minha identidade"
    audio_file = Get-Item -Path ".\audio_verify.wav"
}

Invoke-RestMethod -Uri "http://localhost:8000/voice/verify" `
    -Method POST `
    -Form $formData
```

---

### Python Script de Teste

```python
import requests

BASE_URL = "http://localhost:8000"

# 1. Obter frase de desafio
response = requests.get(f"{BASE_URL}/voice/challenge")
challenge = response.json()
print(f"Frase: {challenge['phrase']}")

# 2. Enrollment
with open('audio.wav', 'rb') as audio:
    files = {'audio_file': audio}
    data = {
        'user_id': 'user123',
        'phrase_expected': challenge['phrase']
    }
    response = requests.post(f"{BASE_URL}/voice/enroll", files=files, data=data)
    print(f"Enrollment: {response.json()}")

# 3. Verificação
with open('audio_verify.wav', 'rb') as audio:
    files = {'audio_file': audio}
    data = {
        'user_id': 'user123',
        'phrase_expected': challenge['phrase']
    }
    response = requests.post(f"{BASE_URL}/voice/verify", files=files, data=data)
    result = response.json()
    print(f"Autenticado: {result['authenticated']}")
    print(f"Similaridade: {result['similarity']}")
```

---

### JavaScript/Node.js

```javascript
const FormData = require('form-data');
const fs = require('fs');
const axios = require('axios');

const BASE_URL = 'http://localhost:8000';

async function testVoiceAuth() {
    // 1. Obter frase
    const challengeRes = await axios.get(`${BASE_URL}/voice/challenge`);
    console.log('Frase:', challengeRes.data.phrase);

    // 2. Enrollment
    const enrollForm = new FormData();
    enrollForm.append('user_id', 'user123');
    enrollForm.append('phrase_expected', challengeRes.data.phrase);
    enrollForm.append('audio_file', fs.createReadStream('audio.wav'));

    const enrollRes = await axios.post(`${BASE_URL}/voice/enroll`, enrollForm, {
        headers: enrollForm.getHeaders()
    });
    console.log('Enrollment:', enrollRes.data);

    // 3. Verificação
    const verifyForm = new FormData();
    verifyForm.append('user_id', 'user123');
    verifyForm.append('phrase_expected', challengeRes.data.phrase);
    verifyForm.append('audio_file', fs.createReadStream('audio_verify.wav'));

    const verifyRes = await axios.post(`${BASE_URL}/voice/verify`, verifyForm, {
        headers: verifyForm.getHeaders()
    });
    console.log('Verificação:', verifyRes.data);
}

testVoiceAuth();
```

---

## Testando com Docker Compose

### 1. Construir e iniciar
```bash
docker-compose up --build
```

### 2. Ver logs
```bash
docker-compose logs -f app
```

### 3. Parar serviços
```bash
docker-compose down
```

### 4. Limpar volumes
```bash
docker-compose down -v
```

---

## Gravar Áudio de Teste

### Usando FFmpeg (converter qualquer áudio para WAV)
```bash
ffmpeg -i input.mp3 -ar 16000 -ac 1 -f wav output.wav
```

### Usando Python (gravar do microfone)
```python
import sounddevice as sd
import scipy.io.wavfile as wav

# Configurações
duration = 3  # segundos
sample_rate = 16000

print("Gravando... Fale agora!")
audio = sd.rec(int(duration * sample_rate), 
               samplerate=sample_rate, 
               channels=1)
sd.wait()
print("Gravação finalizada!")

# Salvar
wav.write('audio.wav', sample_rate, audio)
```

---

## Verificando o Banco de Dados

### Conectar ao MySQL no container
```bash
docker exec -it auth_voice_mysql mysql -uroot -prootpassword auth_voice_db
```

### Ver perfis cadastrados
```sql
SELECT id, user_id, created_at FROM user_voice_profile;
```

### Ver embedding de um usuário
```sql
SELECT user_id, JSON_LENGTH(embedding) as embedding_size 
FROM user_voice_profile 
WHERE user_id = 'user123';
```

---

## Health Check

```bash
curl http://localhost:8000/health
```

---

## Acessar Documentação Interativa

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

Na interface Swagger você pode testar todos os endpoints interativamente!
