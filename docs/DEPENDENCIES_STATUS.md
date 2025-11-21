# Dependências Instaladas e Necessárias

## ✅ Instaladas e Funcionando (Ambiente Atual)

### Core Framework
- fastapi==0.115.12 ✅
- uvicorn==0.34.2 ✅
- python-multipart==0.0.6 ✅

### Database
- sqlalchemy==2.0.41 ✅
- pymysql==1.1.0 ✅
- cryptography==41.0.7 ✅

### Configuration
- python-dotenv==1.0.0 ✅
- pydantic==2.11.5 ✅
- pydantic-settings==2.1.0 ✅

### Utilities
- requests==2.31.0 ✅

---

## ⚠️ NÃO Instaladas (Dependências de ML - PESADAS)

### Machine Learning / Voice Processing
- vosk (~500MB) - Reconhecimento de fala
- speechbrain (~1GB) - Extração de embeddings vocais
- torch (~2GB) - Framework de deep learning
- torchaudio (~500MB) - Processamento de áudio
- numpy (~50MB) - Computação numérica
- scikit-learn (~100MB) - Similaridade de cosseno

**Total estimado: ~4GB de download**

---

## 📊 Status Atual

### API de Teste (Funcionando)
- ✅ Servidor FastAPI rodando
- ✅ Endpoints básicos funcionando
- ✅ CORS configurado
- ✅ MySQL conectado
- ✅ Pronta para testar com Expo

### Funcionalidades Disponíveis
- ✅ GET / - Info da API
- ✅ GET /health - Health check
- ✅ GET /voice/challenge - Retorna frase de teste

### Funcionalidades que Precisam de ML
- ❌ POST /voice/enroll - Cadastro de voz (precisa de vosk + speechbrain)
- ❌ POST /voice/verify - Verificação de voz (precisa de vosk + speechbrain)

---

## 🚀 Para Instalar Dependências de ML (Se Necessário)

### Opção 1: Instalar Apenas o Necessário
```bash
pip install vosk speechbrain torch torchaudio numpy scikit-learn
```

### Opção 2: Instalar do requirements.txt
```bash
# Descomente as linhas de ML no requirements.txt e execute:
pip install -r requirements.txt
```

### Opção 3: Instalar Tudo de Uma Vez (Mais Rápido)
```bash
pip install vosk==0.3.45 speechbrain==0.5.16 torch==2.1.1 torchaudio==2.1.1 numpy==1.24.3 scikit-learn==1.3.2
```

---

## 💡 Recomendação

### Para Desenvolvimento do App Expo:
**NÃO instale as dependências de ML agora.**

Razões:
1. Download grande (~4GB)
2. Instalação demorada (~20-30 min)
3. API de teste já funciona para desenvolver a interface
4. Você pode desenvolver todo o frontend do app primeiro

### Quando Instalar ML:
- Quando quiser testar autenticação real de voz
- Antes de fazer deploy em produção
- Quando a interface do app estiver pronta

---

## 📝 Notas

- Python 3.10.0: ✅ Compatível
- Sistema: Windows 10/11 ✅
- MySQL: ✅ Configurado e funcionando
- API: ✅ Rodando em http://10.1.4.224:8000

---

**Atualizado em:** 19 de novembro de 2025
