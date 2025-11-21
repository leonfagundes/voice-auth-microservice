"""
Script para copiar modelos do HuggingFace Hub sem usar symlinks
Resolve o problema de permissão no Windows
"""
import os
import shutil
from pathlib import Path

# Caminhos
CACHE_DIR = Path.home() / ".cache" / "huggingface" / "hub"
PROJECT_DIR = Path("./models/speechbrain")

def copy_model_files():
    """Copia arquivos do cache do HuggingFace para o diretório do projeto"""
    
    print("=" * 60)
    print("🔧 CORREÇÃO: Copiar Modelos SpeechBrain")
    print("=" * 60)
    print()
    
    # Procurar pelo modelo no cache
    model_cache = CACHE_DIR / "models--speechbrain--spkrec-ecapa-voxceleb"
    
    if not model_cache.exists():
        print("❌ Modelo não encontrado no cache")
        print(f"📁 Procurado em: {model_cache}")
        print()
        print("💡 Execute a API primeiro para baixar o modelo.")
        return False
    
    print(f"✅ Modelo encontrado no cache: {model_cache}")
    print()
    
    # Encontrar o snapshot mais recente
    snapshots_dir = model_cache / "snapshots"
    if not snapshots_dir.exists():
        print("❌ Diretório de snapshots não encontrado")
        return False
    
    # Pegar o primeiro snapshot (mais recente)
    snapshots = list(snapshots_dir.iterdir())
    if not snapshots:
        print("❌ Nenhum snapshot encontrado")
        return False
    
    snapshot = snapshots[0]
    print(f"📦 Usando snapshot: {snapshot.name}")
    print()
    
    # Criar diretório de destino
    PROJECT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Copiar arquivos
    print("📋 Copiando arquivos...")
    files_copied = 0
    errors = []
    
    for file in snapshot.iterdir():
        if file.is_file():
            dest = PROJECT_DIR / file.name
            
            try:
                # Remover arquivo existente se for symlink
                if dest.exists():
                    if dest.is_symlink():
                        dest.unlink()
                        print(f"  🗑️  Removido symlink: {file.name}")
                    else:
                        print(f"  ⏭️  Já existe (arquivo): {file.name}")
                        continue
                
                # Copiar arquivo
                shutil.copy2(file, dest)
                print(f"  ✅ Copiado: {file.name} ({file.stat().st_size} bytes)")
                files_copied += 1
            except Exception as e:
                errors.append(f"{file.name}: {e}")
                print(f"  ❌ Erro ao copiar {file.name}: {e}")
    
    print()
    print("=" * 60)
    if errors:
        print(f"⚠️  {files_copied} arquivos copiados com {len(errors)} erros")
        print()
        print("Erros:")
        for error in errors:
            print(f"  - {error}")
    else:
        print(f"🎉 {files_copied} arquivos copiados com sucesso!")
    print("=" * 60)
    print()
    print("✨ Agora reinicie a API")
    print()
    
    return True

if __name__ == "__main__":
    try:
        copy_model_files()
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
