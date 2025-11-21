# 🧪 Como Testar a API Sem App

Várias formas de testar a API de autenticação por voz sem precisar do app mobile:

---

## 📋 **OPÇÃO 1: Swagger UI (Mais Fácil!)** ⭐

### 1. Inicie a API
```powershell
.\venv\Scripts\activate
python start_api.py
```

### 2. Abra o navegador
```
http://localhost:8000/docs
```

### 3. Teste os endpoints interativamente

#### **GET /voice/challenge**
1. Clique em "GET /voice/challenge"
2. Clique em "Try it out"
3. Clique em "Execute"
4. Copie a frase retornada

#### **POST /voice/enroll**
1. Clique em "POST /voice/enroll"
2. Clique em "Try it out"
3. Preencha:
   - `user_id`: "usuario_teste"
   - `phrase_expected`: (cole a frase do challenge)
   - `audio_file`: Clique em "Choose File" e selecione um arquivo WAV
4. Clique em "Execute"

#### **POST /voice/verify**
1. Clique em "POST /voice/verify"
2. Clique em "Try it out"
3. Preencha os mesmos dados do enroll
4. Execute e veja o resultado da autenticação

---

## 🐍 **OPÇÃO 2: Script Python (test_api.py)**

### 1. Prepare um arquivo de áudio
Grave um áudio WAV dizendo uma das frases:
- "Minha voz é minha identidade"
- "Autenticação segura por voz"

Salve como `test_audio.wav` na raiz do projeto.

### 2. Execute o teste
```powershell
.\venv\Scripts\activate
python test_api.py
```

O script vai:
- ✅ Verificar se a API está online
- ✅ Obter uma frase de desafio
- ✅ Fazer enrollment com seu áudio
- ✅ Verificar a autenticação

---

## 🌐 **OPÇÃO 3: cURL (Terminal)**

### 1. Get Challenge
```powershell
curl http://localhost:8000/voice/challenge
```

**Resposta**:
```json
{"phrase":"Minha voz é minha identidade"}
```

### 2. Enroll User
```powershell
curl -X POST "http://localhost:8000/voice/enroll" `
  -F "user_id=usuario123" `
  -F "phrase_expected=Minha voz é minha identidade" `
  -F "audio_file=@test_audio.wav"
```

### 3. Verify User
```powershell
curl -X POST "http://localhost:8000/voice/verify" `
  -F "user_id=usuario123" `
  -F "phrase_expected=Minha voz é minha identidade" `
  -F "audio_file=@test_audio.wav"
```

---

## 📬 **OPÇÃO 4: Postman**

### 1. Importe a coleção

Crie uma nova coleção com estas requisições:

#### **GET Challenge**
- Method: GET
- URL: `http://localhost:8000/voice/challenge`

#### **POST Enroll**
- Method: POST
- URL: `http://localhost:8000/voice/enroll`
- Body: form-data
  - `user_id`: usuario123
  - `phrase_expected`: Minha voz é minha identidade
  - `audio_file`: [arquivo WAV]

#### **POST Verify**
- Method: POST
- URL: `http://localhost:8000/voice/verify`
- Body: form-data (mesmos campos do enroll)

---

## 🎤 **OPÇÃO 5: Gravar Áudio Direto do Python**

Use o script `gravar_audio.py` criado:

```powershell
.\venv\Scripts\activate
python gravar_audio.py
```

Ele vai:
1. Obter uma frase da API
2. Mostrar a frase para você ler
3. Gravar 3 segundos de áudio
4. Salvar como `gravacao.wav`
5. Automaticamente fazer enrollment E verificação!

---

## 🔧 **OPÇÃO 6: Script Completo Automatizado**

Use o script `test_completo.py`:

```powershell
.\venv\Scripts\activate
python test_completo.py
```

Este script:
- ✅ Cria áudio sintético para teste
- ✅ Testa todos os endpoints
- ✅ Mostra resultados detalhados
- ✅ Não precisa de gravação manual

---

## 📊 **OPÇÃO 7: Thunder Client (VS Code)**

Se usa VS Code:

1. Instale a extensão "Thunder Client"
2. Crie uma nova requisição
3. Configure como no Postman acima

---

## 🎯 **Recomendação por Cenário**

| Cenário | Melhor Opção |
|---------|--------------|
| Teste rápido e visual | ⭐ **Swagger UI** (Opção 1) |
| Teste automatizado | 🐍 **test_api.py** (Opção 2) |
| Teste com áudio real | 🎤 **gravar_audio.py** (Opção 5) |
| CI/CD / Scripts | 🌐 **cURL** (Opção 3) |
| Desenvolvimento/Debug | 📬 **Postman** (Opção 4) |
| Teste sem áudio real | 🔧 **test_completo.py** (Opção 6) |

---

## 📝 **Dicas Importantes**

### Formato do Áudio
- ✅ **Formato**: WAV (recomendado)
- ✅ **Sample Rate**: 16000 Hz (ideal)
- ✅ **Canais**: Mono (1 canal)
- ✅ **Duração**: 2-5 segundos

### Qualidade do Áudio
- 🎤 Fale claramente
- 🔇 Evite ruídos de fundo
- 📱 Use um microfone decente
- 🗣️ Pronuncie a frase completa

### Solução de Problemas
```python
# Se der erro de "áudio vazio"
- Verifique se o arquivo não está corrompido
- Tente converter para WAV com: ffmpeg -i input.mp3 -ar 16000 -ac 1 output.wav

# Se der erro de "transcrição não corresponde"
- Fale mais devagar e claramente
- Pronuncie exatamente a frase retornada
- Verifique se não há ruído de fundo

# Se der erro de "não autenticado"
- Threshold padrão é 0.75 (75% de similaridade)
- Use o MESMO usuário no enroll e verify
- Tente gravar em ambiente silencioso
```

---

## 🚀 **Quick Start (30 segundos)**

```powershell
# 1. Inicie a API
.\venv\Scripts\activate
python start_api.py

# 2. Abra em outro terminal
.\venv\Scripts\activate
python test_completo.py
```

Pronto! ✨

---

## 📚 **Mais Recursos**

- 📖 Documentação da API: http://localhost:8000/docs
- 📘 ReDoc: http://localhost:8000/redoc
- 📗 Exemplos: `EXAMPLES.md`
- 📕 README: `README.md`
