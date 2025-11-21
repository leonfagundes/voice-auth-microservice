# 🛠️ Scripts do Projeto

Coleção de scripts para configuração, teste e manutenção do projeto.

---

## 🚀 **Scripts de Inicialização**

### `start_api.py`
Inicia a API FastAPI com Uvicorn.

```bash
python scripts/start_api.py
```

**Acesso**:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- API: http://localhost:8000

### `run_local.py`
Execução local alternativa da API.

```bash
python scripts/run_local.py
```

---

## 🧪 **Scripts de Teste**

### `teste_rapido.py` ⚡ **RECOMENDADO**
Teste ultra-rápido para verificar se a API está funcionando.

```bash
python scripts/teste_rapido.py
```

**Testa**:
- ✅ Health check
- ✅ Endpoint de challenge

**Duração**: ~30 segundos

---

### `test_completo.py` 🔧
Teste completo automatizado com áudio sintético.

```bash
python scripts/test_completo.py
```

**Testa**:
- ✅ Conexão com API
- ✅ Challenge phrase
- ✅ Enrollment
- ✅ Verificação

**Vantagem**: Não precisa gravar áudio!

---

### `gravar_audio.py` 🎤
Grava áudio real e testa enrollment + verificação.

```bash
# Instale sounddevice primeiro
pip install sounddevice

# Execute
python scripts/gravar_audio.py
```

**Processo**:
1. Obtém frase de desafio
2. Grava 3 segundos de áudio
3. Faz enrollment
4. Testa verificação

**Ideal para**: Teste com áudio real do usuário

---

### `test_api.py`
Teste completo usando arquivo de áudio WAV.

```bash
# Prepare um arquivo test_audio.wav
python scripts/test_api.py
```

**Requer**: Arquivo `test_audio.wav` na raiz do projeto

---

### `test_db_connection.py`
Testa a conexão com o banco de dados MySQL.

```bash
python scripts/test_db_connection.py
```

**Verifica**:
- ✅ Conexão com MySQL
- ✅ Criação de tabelas
- ✅ Operações CRUD

---

### `test_embeddings_final.py`
Testa a extração de embeddings de voz.

```bash
python scripts/test_embeddings_final.py
```

**Verifica**:
- ✅ Áudio sintético criado
- ✅ Embedding extraído (192 dimensões)
- ✅ Similaridade calculada

---

### `test_speechbrain_api.py`
Teste de compatibilidade com SpeechBrain 1.0+.

```bash
python scripts/test_speechbrain_api.py
```

**Verifica**:
- ✅ Import correto (`speechbrain.inference.speaker`)
- ✅ Modelo carregado
- ✅ `encode_batch` funcionando
- ✅ Embedding com dimensão correta

---

### `test_simple_api.py`
Teste simples dos endpoints básicos.

```bash
python scripts/test_simple_api.py
```

---

## ⚙️ **Scripts de Configuração**

### `download_vosk_model.py`
Baixa o modelo Vosk para reconhecimento de fala.

```bash
python scripts/download_vosk_model.py
```

**Modelo**: vosk-model-small-pt-0.3 (Português)  
**Destino**: `./models/vosk-model-small-pt-0.3/`

---

### `fix_speechbrain_symlink.py`
Corrige problemas de symlinks do SpeechBrain no Windows.

```bash
python scripts/fix_speechbrain_symlink.py
```

**Resolve**:
- ❌ Erro de permissão ao criar symlinks
- ❌ Modelos não carregando corretamente

---

### `copy_all_speechbrain_files.py`
Copia todos os arquivos do modelo SpeechBrain.

```bash
python scripts/copy_all_speechbrain_files.py
```

**Uso**: Quando `fix_speechbrain_symlink.py` não resolver

---

## 📊 **Comparação dos Testes**

| Script | Velocidade | Requer Áudio | Automático | Ideal Para |
|--------|------------|--------------|------------|------------|
| `teste_rapido.py` | ⚡⚡⚡ | ❌ | ✅ | Verificação rápida |
| `test_completo.py` | ⚡⚡ | ❌ | ✅ | Teste completo sem áudio |
| `gravar_audio.py` | ⚡ | ✅ (grava) | ✅ | Teste com voz real |
| `test_api.py` | ⚡⚡ | ✅ (arquivo) | ✅ | Teste com WAV existente |
| `test_embeddings_final.py` | ⚡⚡ | ❌ | ✅ | Validar ML pipeline |
| `test_speechbrain_api.py` | ⚡⚡ | ❌ | ✅ | Verificar compatibilidade |

---

## 🎯 **Fluxo de Uso Recomendado**

### 1️⃣ **Primeira Vez**
```bash
# Baixar modelos
python scripts/download_vosk_model.py

# Corrigir symlinks (Windows)
python scripts/fix_speechbrain_symlink.py

# Iniciar API
python scripts/start_api.py
```

### 2️⃣ **Teste Rápido**
```bash
# Terminal 1
python scripts/start_api.py

# Terminal 2
python scripts/teste_rapido.py
```

### 3️⃣ **Teste Completo**
```bash
# Com áudio sintético (mais rápido)
python scripts/test_completo.py

# OU com sua voz (mais realista)
python scripts/gravar_audio.py
```

### 4️⃣ **Desenvolvimento**
```bash
# Testar banco de dados
python scripts/test_db_connection.py

# Testar embeddings
python scripts/test_embeddings_final.py

# Testar SpeechBrain
python scripts/test_speechbrain_api.py
```

---

## 📝 **Notas Importantes**

### Caminhos Relativos
Todos os scripts devem ser executados a partir da **raiz do projeto**:

```bash
# ✅ CORRETO
python scripts/start_api.py

# ❌ ERRADO
cd scripts
python start_api.py
```

### Ambiente Virtual
Sempre ative o ambiente virtual antes:

```bash
# Windows
.\venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### Dependências Opcionais
Alguns scripts requerem dependências extras:

```bash
# Para gravar_audio.py
pip install sounddevice
```

---

## 🆘 **Troubleshooting**

### Script não encontra módulos
```bash
# Certifique-se de estar na raiz do projeto
cd c:\Users\leonf\OneDrive\Desktop\-\repositorios\auth-voice

# Ative o ambiente virtual
.\venv\Scripts\activate

# Execute o script
python scripts/nome_do_script.py
```

### Erro de permissão (Windows)
```bash
# Execute o fix de symlink
python scripts/fix_speechbrain_symlink.py
```

### API não inicia
```bash
# Verifique se a porta 8000 está livre
netstat -ano | findstr :8000

# Teste conexão com banco
python scripts/test_db_connection.py
```

---

## 📚 **Mais Informações**

- 📖 **Documentação completa**: [../docs/README.md](../docs/README.md)
- 🧪 **Guia de testes**: [../docs/TESTES_SEM_APP.md](../docs/TESTES_SEM_APP.md)
- 🚀 **Quick Start**: [../docs/QUICKSTART.md](../docs/QUICKSTART.md)

---

**Última atualização**: 20 de novembro de 2025
