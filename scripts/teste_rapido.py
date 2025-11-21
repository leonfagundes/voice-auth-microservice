"""
Script ultra-simples para teste rápido da API
Apenas verifica se está funcionando
"""
import requests

print("🔍 Testando API...")

try:
    # Teste 1: Health
    r = requests.get("http://localhost:8000/health", timeout=5)
    print(f"✅ Health: {r.json()}")
    
    # Teste 2: Challenge
    r = requests.get("http://localhost:8000/voice/challenge")
    print(f"✅ Challenge: {r.json()['phrase']}")
    
    print("\n🎉 API está funcionando!")
    print("📚 Veja TESTES_SEM_APP.md para mais opções de teste")
    print("🌐 Documentação: http://localhost:8000/docs")
    
except Exception as e:
    print(f"❌ Erro: {e}")
    print("\n💡 Inicie a API com:")
    print("   python start_api.py")
