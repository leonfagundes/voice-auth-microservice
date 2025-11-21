"""Script para iniciar a API Voice Authentication"""
import os
import sys
import logging
import warnings

warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", message="torchaudio._backend.set_audio_backend")
warnings.filterwarnings("ignore", message="The torchaudio backend is switched")
warnings.filterwarnings("ignore", message="torchvision is not available")

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_environment():
    """Verifica se o ambiente está configurado corretamente"""
    logger.info("🔍 Verificando ambiente...")
    
    if not os.path.exists('.env'):
        logger.error("❌ Arquivo .env não encontrado!")
        return False
    
    if not os.path.exists('phrases.txt'):
        logger.warning("⚠️  phrases.txt não encontrado. Usando frases padrão.")
    
    try:
        import fastapi
        import uvicorn
        import sqlalchemy
        logger.info("✅ Dependências básicas OK")
    except ImportError as e:
        logger.error(f"❌ Faltam dependências: {e}")
        return False
    
    try:
        import vosk
        import speechbrain
        import torch
        logger.info("✅ Dependências ML OK (vosk, speechbrain, torch)")
    except ImportError as e:
        logger.warning(f"⚠️  Dependências ML não instaladas: {e}")
        logger.info("ℹ️  A API funcionará mas sem recursos de voz completos")
    
    return True

def main():
    """Função principal"""
    print("=" * 60)
    print("🎙️  VOICE AUTHENTICATION API")
    print("=" * 60)
    print()
    
    if not check_environment():
        logger.error("❌ Ambiente não está configurado corretamente!")
        logger.info("ℹ️  Execute: pip install -r requirements.txt")
        sys.exit(1)
    
    logger.info("🚀 Iniciando servidor...")
    print()
    
    import uvicorn
    from app.config import get_settings
    
    settings = get_settings()
    
    try:
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=settings.app_port,
            reload=settings.debug,
            log_level="info"
        )
    except KeyboardInterrupt:
        logger.info("\n👋 Servidor encerrado pelo usuário")
    except Exception as e:
        logger.error(f"❌ Erro ao iniciar servidor: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
