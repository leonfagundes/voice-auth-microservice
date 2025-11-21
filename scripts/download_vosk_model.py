"""Script para baixar o modelo Vosk em português"""
import os
import sys
import zipfile
import urllib.request
from pathlib import Path

MODEL_NAME = "vosk-model-small-pt-0.3"
MODEL_URL = f"https://alphacephei.com/vosk/models/{MODEL_NAME}.zip"
MODELS_DIR = Path("./models")
MODEL_PATH = MODELS_DIR / MODEL_NAME

def download_with_progress(url, filename):
    """Baixa arquivo com barra de progresso"""
    def reporthook(count, block_size, total_size):
        percent = int(count * block_size * 100 / total_size)
        sys.stdout.write(f"\r📥 Baixando... {percent}%")
        sys.stdout.flush()
    
    urllib.request.urlretrieve(url, filename, reporthook)
    print()

def main():
    print("=" * 60)
    print("🎙️  DOWNLOAD DO MODELO VOSK - PORTUGUÊS")
    print("=" * 60)
    print()
    
    # Verificar se já existe
    if MODEL_PATH.exists():
        print(f"✅ Modelo já existe em: {MODEL_PATH}")
        response = input("Deseja baixar novamente? (s/n): ").lower()
        if response != 's':
            print("✨ Usando modelo existente!")
            return
        print("🗑️  Removendo modelo antigo...")
        import shutil
        shutil.rmtree(MODEL_PATH)
    
    # Criar diretório
    print(f"📁 Criando diretório: {MODELS_DIR}")
    MODELS_DIR.mkdir(exist_ok=True)
    
    # Baixar modelo
    print(f"🌐 Baixando de: {MODEL_URL}")
    print(f"📦 Tamanho aproximado: ~31 MB")
    print()
    
    zip_path = MODELS_DIR / f"{MODEL_NAME}.zip"
    
    try:
        download_with_progress(MODEL_URL, zip_path)
        print(f"✅ Download concluído: {zip_path}")
    except Exception as e:
        print(f"❌ Erro ao baixar: {e}")
        print()
        print("💡 SOLUÇÃO MANUAL:")
        print(f"1. Acesse: {MODEL_URL}")
        print(f"2. Baixe o arquivo ZIP")
        print(f"3. Extraia para: {MODELS_DIR}")
        sys.exit(1)
    
    # Extrair
    print()
    print(f"📂 Extraindo modelo...")
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(MODELS_DIR)
        print(f"✅ Modelo extraído em: {MODEL_PATH}")
    except Exception as e:
        print(f"❌ Erro ao extrair: {e}")
        sys.exit(1)
    
    # Remover ZIP
    print(f"🗑️  Removendo arquivo ZIP...")
    zip_path.unlink()
    
    # Verificar
    if MODEL_PATH.exists():
        print()
        print("=" * 60)
        print("🎉 MODELO INSTALADO COM SUCESSO!")
        print("=" * 60)
        print()
        print(f"📍 Localização: {MODEL_PATH.absolute()}")
        print(f"📝 Configurado em .env: VOSK_MODEL_PATH={MODEL_PATH}")
        print()
        print("✨ Reinicie a API para usar o modelo!")
        print("   Comando: python start_api.py")
        print()
    else:
        print("❌ Erro: Modelo não encontrado após extração")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Download cancelado pelo usuário")
        sys.exit(0)
