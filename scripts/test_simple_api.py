"""
Versão simplificada da API para testar sem dependências de ML
"""
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Criar aplicação FastAPI
app = FastAPI(
    title="Voice Authentication API - Test Mode",
    description="API de autenticação por voz (modo teste - sem ML)",
    version="1.0.0-test"
)

# Configurar CORS - Permitir Expo Go
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Endpoint raiz"""
    return {
        "message": "Voice Authentication API - Test Mode",
        "version": "1.0.0-test",
        "status": "running",
        "note": "Versão de teste sem dependências de ML"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "mode": "test",
        "database": "not configured in test mode"
    }

@app.get("/voice/challenge")
async def get_challenge():
    """Retorna uma frase de desafio"""
    return {
        "phrase": "Minha voz é minha identidade - TESTE"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "test_simple_api:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
