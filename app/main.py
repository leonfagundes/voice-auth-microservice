"""
Aplicação principal FastAPI
"""
import logging
import os
import warnings
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

warnings.filterwarnings("ignore", category=UserWarning, module="speechbrain")
warnings.filterwarnings("ignore", message="torchaudio._backend.set_audio_backend")
warnings.filterwarnings("ignore", message="torchvision is not available")

from app.config import get_settings
from app.database import init_db
from app.routers import voice

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gerencia o ciclo de vida da aplicação (startup e shutdown)
    """
    logger.info("🚀 Iniciando aplicação Voice Authentication API...")
    
    try:
        init_db()
        logger.info("✅ Banco de dados inicializado com sucesso")
    except Exception as e:
        logger.error(f"❌ Erro ao inicializar banco de dados: {e}")
        raise
    
    phrases_file = "phrases.txt"
    if os.path.exists(phrases_file):
        try:
            from app.services.voice_service import VoiceService
            from app.database import SessionLocal
            db = SessionLocal()
            try:
                service = VoiceService(db)
                service.load_phrases_from_file(phrases_file)
                logger.info("✅ Frases de desafio carregadas")
            finally:
                db.close()
        except Exception as e:
            logger.warning(f"⚠️  Erro ao carregar frases: {e}")
    else:
        logger.info("ℹ️  Usando frases padrão (phrases.txt não encontrado)")
    
    logger.info("=" * 60)
    logger.info("✨ API INICIADA COM SUCESSO!")
    logger.info(f"📡 Acesse: http://localhost:8000/docs")
    logger.info(f"📱 Expo Go: http://10.1.4.224:8000")
    logger.info("=" * 60)
    
    yield
    
    logger.info("👋 Encerrando aplicação...")



app = FastAPI(
    title="Voice Authentication API",
    description="API de autenticação por voz usando SpeechBrain e Vosk",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(voice.router)


@app.get("/")
async def root():
    """Endpoint raiz"""
    return {
        "message": "Voice Authentication API",
        "version": "1.0.0",
        "endpoints": {
            "challenge": "/voice/challenge",
            "enroll": "/voice/enroll",
            "verify": "/voice/verify",
            "docs": "/docs"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "database": "connected"
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=settings.debug
    )
