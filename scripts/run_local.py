#!/usr/bin/env python
"""
Script para executar a aplicação localmente (sem Docker)
"""
import os
import sys
from pathlib import Path

def check_python_version():
    """Verifica se a versão do Python é compatível"""
    if sys.version_info < (3, 10):
        print("❌ Python 3.10+ é necessário")
        print(f"   Versão atual: {sys.version}")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}")
    return True


def check_env_file():
    """Verifica se arquivo .env existe"""
    env_file = Path(".env")
    if not env_file.exists():
        print("⚠️  Arquivo .env não encontrado!")
        print("   Copiando .env.example para .env...")
        
        example_file = Path(".env.example")
        if example_file.exists():
            import shutil
            shutil.copy(".env.example", ".env")
            print("✅ Arquivo .env criado")
            print("   ⚙️  Configure as variáveis de ambiente no arquivo .env")
            return True
        else:
            print("❌ Arquivo .env.example não encontrado")
            return False
    
    print("✅ Arquivo .env encontrado")
    return True


def check_vosk_model():
    """Verifica se modelo Vosk está presente"""
    model_path = Path("models/vosk-model-small-pt-0.3")
    
    if not model_path.exists():
        print("⚠️  Modelo Vosk não encontrado!")
        print("   Baixe de: https://alphacephei.com/vosk/models")
        print("   Extraia em: ./models/vosk-model-small-pt-0.3")
        return False
    
    print("✅ Modelo Vosk encontrado")
    return True


def install_dependencies():
    """Instala dependências"""
    print("\n📦 Verificando dependências...")
    
    try:
        import fastapi
        import sqlalchemy
        print("✅ Dependências principais instaladas")
        return True
    except ImportError:
        print("⚠️  Algumas dependências não estão instaladas")
        response = input("   Deseja instalar agora? (s/n): ")
        
        if response.lower() == 's':
            print("   Instalando dependências...")
            os.system(f"{sys.executable} -m pip install -r requirements.txt")
            print("✅ Dependências instaladas")
            return True
        else:
            print("❌ Instale as dependências com: pip install -r requirements.txt")
            return False


def run_server():
    """Executa o servidor"""
    print("\n🚀 Iniciando servidor...")
    print("   URL: http://localhost:8000")
    print("   Docs: http://localhost:8000/docs")
    print("   Pressione Ctrl+C para parar\n")
    
    try:
        import uvicorn
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=8000,
            reload=True
        )
    except KeyboardInterrupt:
        print("\n\n👋 Servidor encerrado")
    except Exception as e:
        print(f"\n❌ Erro ao iniciar servidor: {e}")


def main():
    """Função principal"""
    print("="*60)
    print("🎙️  VOICE AUTHENTICATION API - Setup Local")
    print("="*60)
    print()
    
    # Verificações
    if not check_python_version():
        return
    
    if not check_env_file():
        return
    
    if not install_dependencies():
        return
    
    # Avisos opcionais
    check_vosk_model()
    
    print("\n" + "="*60)
    
    # Executar servidor
    run_server()


if __name__ == "__main__":
    main()
