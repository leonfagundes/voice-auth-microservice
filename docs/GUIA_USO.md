# 🚀 GUIA RÁPIDO DE USO

## ✅ CORREÇÕES APLICADAS

1. ✅ Warnings do torchaudio suprimidos
2. ✅ Warnings do torchvision suprimidos  
3. ✅ Logs de startup melhorados com emojis
4. ✅ Script `start_api.py` criado com verificações
5. ✅ Melhor tratamento de erros no startup

---

## 🎯 COMO INICIAR A API

### Opção 1: Script Recomendado
```bash
python start_api.py
```

### Opção 2: Uvicorn Direto
```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Opção 3: Python Main
```bash
python -m app.main
```

---

## 📊 SAÍDA ESPERADA

### ✅ Inicialização com Sucesso:
```
============================================================
🎙️  VOICE AUTHENTICATION API
============================================================

🔍 Verificando ambiente...
✅ Dependências básicas OK
✅ Dependências ML OK (vosk, speechbrain, torch)
🚀 Iniciando servidor...

INFO:     Will watch for changes in these directories: ['...']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx] using StatReload
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
🚀 Iniciando aplicação Voice Authentication API...
✅ Banco de dados inicializado com sucesso
✅ Frases de desafio carregadas
============================================================
✨ API INICIADA COM SUCESSO!
📡 Acesse: http://localhost:8000/docs
📱 Expo Go: http://10.1.4.224:8000
============================================================
INFO:     Application startup complete.
```

### ⚠️ Warnings Removidos:
- ❌ "The torchaudio backend is switched to 'soundfile'"
- ❌ "torchaudio._backend.set_audio_backend has been deprecated"
- ❌ "torchvision is not available"

**Esses warnings NÃO aparecerão mais!**

---

## 🔍 VERIFICAR SE ESTÁ FUNCIONANDO

### 1. Testar Localmente
```bash
# PowerShell
Invoke-RestMethod http://localhost:8000/health

# Ou no navegador
http://localhost:8000/docs
```

### 2. Testar do Celular (mesmo WiFi)
```
http://10.1.4.224:8000/health
```

### 3. Endpoints Disponíveis
- GET `/` - Informações da API
- GET `/health` - Health check
- GET `/docs` - Documentação Swagger
- GET `/voice/challenge` - Frase aleatória
- POST `/voice/enroll` - Cadastrar voz
- POST `/voice/verify` - Verificar voz

---

## ❌ SOLUÇÃO DE PROBLEMAS

### Problema: "Não foi possível resolver a importação fastapi"
**Causa:** Editor não detectou o venv
**Solução:** Isso é apenas warning do editor. A API funcionará normalmente.

### Problema: API encerra logo após iniciar
**Causa:** Você apertou Ctrl+C ou erro no código
**Solução:** 
1. Verifique se não há erros de sintaxe
2. Use `python start_api.py` para diagnóstico
3. Veja logs completos

### Problema: ModuleNotFoundError
**Causa:** Dependências não instaladas
**Solução:**
```bash
pip install -r requirements.txt
```

### Problema: "Modelo Vosk não encontrado"
**Causa:** Modelo de voz não baixado
**Solução:**
1. Baixe: https://alphacephei.com/vosk/models
2. Escolha: vosk-model-pt-fb-v0.1.1-20220516_2113 (português)
3. Extraia na pasta `vosk-model-pt`
4. Configure no `.env`: `VOSK_MODEL_PATH=vosk-model-pt`

---

## ✨ DIFERENÇAS ENTRE AS VERSÕES

### `test_simple_api.py` (Teste)
- ✅ Sem ML (leve, rápido)
- ✅ Endpoints básicos (/health, /challenge)
- ✅ Dados mockados
- ❌ Sem enrollment/verificação real

### `app/main.py` (Completo)
- ✅ Com ML (Vosk + SpeechBrain)
- ✅ Todos os endpoints
- ✅ Autenticação real por voz
- ⚠️ Requer modelos ML instalados

---

## 🎉 PRÓXIMOS PASSOS

1. ✅ **API funcionando** (você está aqui!)
2. 📱 **Desenvolver app Expo** com o prompt criado
3. 🧪 **Testar endpoints** básicos primeiro
4. 🎙️ **Implementar gravação** de áudio no app
5. 🔐 **Testar autenticação** completa

---

## 📝 NOTAS IMPORTANTES

1. **Warnings são normais durante import do PyTorch/SpeechBrain**
   - Agora suprimidos ✅
   
2. **"Exit Code: 0" significa sucesso**
   - API foi encerrada corretamente
   - Não é erro!

3. **Logs do SQLAlchemy são verbosos**
   - Normal durante inicialização
   - Mostra criação de tabelas/índices

4. **CORS configurado para "*"**
   - Permite qualquer origem (desenvolvimento)
   - Em produção, especifique domínios

---

**Criado:** 19/11/2025
**Versão API:** 1.0.0
**Status:** 🟢 FUNCIONANDO
