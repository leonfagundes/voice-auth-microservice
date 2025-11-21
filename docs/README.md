# 📚 Documentação do Projeto

Índice de toda a documentação disponível do projeto Voice Authentication API.

---

## 🔌 **Para Desenvolvedores Frontend**

| Documento | Descrição |
|-----------|-----------|
| [API_REFERENCE.md](API_REFERENCE.md) | 🔌 **Referência completa da API** - Endpoints, exemplos de código, tipos |
| [EXAMPLES.md](EXAMPLES.md) | 💡 Exemplos de integração e uso |
| [EXPO_SETUP_GUIDE.txt](EXPO_SETUP_GUIDE.txt) | 📱 Configuração do Expo (app mobile) |

> 📱 **App de Exemplo**: [voice-auth-app](https://github.com/leonfagundes/voice-auth-app) - Aplicativo React Native/Expo completo

---

## 📖 **Guias de Início Rápido**

| Documento | Descrição |
|-----------|-----------|
| [QUICKSTART.md](QUICKSTART.md) | 🚀 Guia rápido para iniciar o projeto em minutos |
| [GUIA_USO.md](GUIA_USO.md) | 📘 Guia completo de uso da API |
| [TESTES_SEM_APP.md](TESTES_SEM_APP.md) | 🧪 Como testar a API sem app mobile |

---

## 🏗️ **Estrutura e Arquitetura**

| Documento | Descrição |
|-----------|-----------|
| [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) | 📁 Estrutura completa do projeto |
| [INDEX.md](INDEX.md) | 🗂️ Índice geral do projeto |
| [SUMMARY.md](SUMMARY.md) | 📊 Resumo do projeto |

---

## 🔧 **Configuração e Instalação**

| Documento | Descrição |
|-----------|-----------|
| [DEPLOYMENT.md](DEPLOYMENT.md) | 🚀 Guia de deploy da aplicação |
| [DEPENDENCIES_STATUS.md](DEPENDENCIES_STATUS.md) | 📦 Status das dependências |
| [MODELO_INSTALADO.md](MODELO_INSTALADO.md) | 🤖 Informações sobre os modelos de ML |

---

## ✅ **Verificação e Testes**

| Documento | Descrição |
|-----------|-----------|
| [CHECKLIST.md](CHECKLIST.md) | ✅ Checklist de implementação |
| [STATUS_ATUAL.md](STATUS_ATUAL.md) | 📊 Status atual do desenvolvimento |
| [AUDITORIA_CODIGO.md](AUDITORIA_CODIGO.md) | 🔍 Relatório de auditoria de código |

---

## 💡 **Referência Rápida**

| Documento | Descrição |
|-----------|-----------|
| [API_REFERENCE.md](API_REFERENCE.md) | 🔌 Referência completa da API (endpoints, códigos, exemplos) |
| [EXAMPLES.md](EXAMPLES.md) | 💻 Exemplos práticos de uso |

---

## 🛠️ **Scripts Disponíveis**

Todos os scripts estão na pasta `../scripts/`

### Scripts de Inicialização
- `start_api.py` - Inicia a API FastAPI
- `run_local.py` - Execução local alternativa

### Scripts de Teste
- `teste_rapido.py` - Teste rápido (30 segundos)
- `test_completo.py` - Teste completo automatizado
- `test_api.py` - Teste com arquivo de áudio
- `gravar_audio.py` - Grava áudio e testa
- `test_db_connection.py` - Teste de conexão com banco
- `test_simple_api.py` - Teste simples da API
- `test_embeddings_final.py` - Teste de extração de embeddings
- `test_speechbrain_api.py` - Teste de compatibilidade SpeechBrain

### Scripts de Configuração
- `download_vosk_model.py` - Download do modelo Vosk
- `fix_speechbrain_symlink.py` - Correção de symlinks no Windows
- `copy_all_speechbrain_files.py` - Cópia de arquivos do SpeechBrain

---

## 📋 **Arquivos de Configuração**

Na raiz do projeto:
- `requirements.txt` - Dependências Python
- `docker-compose.yml` - Configuração Docker
- `Dockerfile` - Imagem Docker da API
- `Makefile` - Comandos make para automação
- `schema.sql` - Schema do banco de dados
- `phrases.txt` - Frases de desafio para autenticação
- `expo-api-config.js` - Configuração do app Expo

---

## 🎯 **Como Usar Esta Documentação**

### Se você é novo no projeto:
1. Comece com [QUICKSTART.md](QUICKSTART.md)
2. Leia [GUIA_USO.md](GUIA_USO.md)
3. Veja [EXAMPLES.md](EXAMPLES.md)

### Se vai fazer deploy:
1. Leia [DEPLOYMENT.md](DEPLOYMENT.md)
2. Verifique [DEPENDENCIES_STATUS.md](DEPENDENCIES_STATUS.md)
3. Consulte [CHECKLIST.md](CHECKLIST.md)

### Se vai desenvolver:
1. Entenda [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)
2. Revise [AUDITORIA_CODIGO.md](AUDITORIA_CODIGO.md)
3. Execute os scripts de teste

### Se vai testar:
1. Siga [TESTES_SEM_APP.md](TESTES_SEM_APP.md)
2. Use os scripts em `../scripts/`
3. Acesse http://localhost:8000/docs

---

## 🔗 **Links Úteis**

- 📖 **API Docs (Swagger)**: http://localhost:8000/docs
- 📘 **ReDoc**: http://localhost:8000/redoc
- 🌐 **API Root**: http://localhost:8000/
- ❤️ **Health Check**: http://localhost:8000/health

---

## 📞 **Suporte**

Para dúvidas ou problemas:
1. Consulte a documentação relevante acima
2. Verifique [STATUS_ATUAL.md](STATUS_ATUAL.md)
3. Revise [AUDITORIA_CODIGO.md](AUDITORIA_CODIGO.md) para problemas conhecidos

---

**Última atualização**: 20 de novembro de 2025
