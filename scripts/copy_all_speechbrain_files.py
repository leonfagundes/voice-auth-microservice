"""
Script para copiar TODOS os arquivos do modelo SpeechBrain do cache
Solução definitiva para o problema de symlinks no Windows
"""
import os
import shutil
from pathlib import Path

# Caminhos
CACHE_DIR = Path.home() / ".cache" / "huggingface" / "hub"
PROJECT_DIR = Path("./models/speechbrain")
MODEL_NAME = "models--speechbrain--spkrec-ecapa-voxceleb"

def copy_all_files():
    """Copia todos os arquivos do cache para o projeto"""
    
    print("=" * 70)
    print("🚀 SOLUÇÃO DEFINITIVA: Copiar TODOS os Arquivos do SpeechBrain")
    print("=" * 70)
    print()
    
    # Procurar pelo modelo no cache
    model_cache = CACHE_DIR / MODEL_NAME
    
    if not model_cache.exists():
        print("❌ Modelo não encontrado no cache")
        print(f"📁 Esperado em: {model_cache}")
        print()
        print("💡 O modelo será baixado automaticamente na primeira execução da API.")
        print("   Execute este script novamente depois do primeiro erro.")
        return False
    
    print(f"✅ Modelo encontrado: {model_cache}")
    print()
    
    # Encontrar snapshot
    snapshots_dir = model_cache / "snapshots"
    if not snapshots_dir.exists():
        print("❌ Diretório de snapshots não encontrado")
        return False
    
    snapshots = list(snapshots_dir.iterdir())
    if not snapshots:
        print("❌ Nenhum snapshot encontrado")
        return False
    
    snapshot = snapshots[0]
    print(f"📦 Snapshot: {snapshot.name}")
    print()
    
    # Criar diretório de destino
    PROJECT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Copiar TODOS os arquivos
    print("📋 Copiando arquivos...")
    print()
    
    files_copied = 0
    files_skipped = 0
    total_size = 0
    
    for file in snapshot.iterdir():
        if file.is_file():
            dest = PROJECT_DIR / file.name
            file_size = file.stat().st_size
            
            # Se já existe e não é symlink, pular
            if dest.exists() and not dest.is_symlink():
                print(f"  ⏭️  {file.name:30} (já existe, {file_size:,} bytes)")
                files_skipped += 1
                continue
            
            try:
                # Remover se for symlink
                if dest.exists() and dest.is_symlink():
                    dest.unlink()
                    print(f"  🗑️  {file.name:30} (symlink removido)")
                
                # Copiar arquivo
                shutil.copy2(file, dest)
                print(f"  ✅ {file.name:30} ({file_size:,} bytes)")
                files_copied += 1
                total_size += file_size
                
            except Exception as e:
                print(f"  ❌ {file.name:30} ERRO: {e}")
    
    print()
    print("=" * 70)
    print(f"✨ Concluído!")
    print(f"   📊 {files_copied} arquivo(s) copiado(s) ({total_size:,} bytes)")
    print(f"   ⏭️  {files_skipped} arquivo(s) já existente(s)")
    print("=" * 70)
    print()
    
    if files_copied > 0:
        print("🎉 Agora você pode iniciar/reiniciar a API!")
        print("   Execute: python start_api.py")
    else:
        print("ℹ️  Todos os arquivos já estavam presentes")
    
    print()
    
    # Listar arquivos no diretório do projeto
    print("📂 Arquivos em ./models/speechbrain/:")
    for file in sorted(PROJECT_DIR.iterdir()):
        if file.is_file():
            size = file.stat().st_size
            is_link = "→ symlink" if file.is_symlink() else ""
            print(f"   • {file.name:30} {size:>12,} bytes {is_link}")
    
    print()
    return True

if __name__ == "__main__":
    try:
        copy_all_files()
    except KeyboardInterrupt:
        print("\n\n⚠️  Operação cancelada pelo usuário")
    except Exception as e:
        print(f"\n\n❌ Erro inesperado: {e}")
        import traceback
        traceback.print_exc()
