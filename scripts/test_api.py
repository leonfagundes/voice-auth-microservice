"""Script de teste da API de autenticação por voz"""
import requests
import time
from pathlib import Path

BASE_URL = "http://localhost:8000"


def print_separator():
    print("\n" + "="*60 + "\n")


def test_health():
    """Testa se a API está rodando"""
    print("🏥 Testando health check...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ API está online!")
            print(f"Response: {response.json()}")
            return True
        else:
            print(f"❌ API retornou status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao conectar à API: {e}")
        print("Certifique-se de que a API está rodando em http://localhost:8000")
        return False


def get_challenge():
    """Obtém uma frase de desafio"""
    print("🎯 Obtendo frase de desafio...")
    try:
        response = requests.get(f"{BASE_URL}/voice/challenge")
        response.raise_for_status()
        phrase = response.json()["phrase"]
        print(f"✅ Frase obtida: '{phrase}'")
        return phrase
    except Exception as e:
        print(f"❌ Erro ao obter frase: {e}")
        return None


def enroll_user(user_id: str, phrase: str, audio_path: str):
    """Faz enrollment de um usuário"""
    print(f"📝 Fazendo enrollment do usuário '{user_id}'...")
    
    audio_file = Path(audio_path)
    if not audio_file.exists():
        print(f"❌ Arquivo de áudio não encontrado: {audio_path}")
        return False
    
    try:
        with open(audio_path, 'rb') as audio:
            files = {'audio_file': ('audio.wav', audio, 'audio/wav')}
            data = {
                'user_id': user_id,
                'phrase_expected': phrase
            }
            response = requests.post(
                f"{BASE_URL}/voice/enroll", 
                files=files, 
                data=data
            )
            
            result = response.json()
            
            if response.status_code == 200 and result.get('success'):
                print("✅ Enrollment realizado com sucesso!")
                print(f"   - User ID: {result.get('user_id')}")
                print(f"   - Transcrição: {result.get('transcription')}")
                print(f"   - Mensagem: {result.get('message')}")
                return True
            else:
                print(f"❌ Falha no enrollment:")
                print(f"   - Status: {response.status_code}")
                print(f"   - Mensagem: {result.get('message')}")
                if 'transcription' in result:
                    print(f"   - Transcrição: {result['transcription']}")
                    print(f"   - Esperado: {result.get('expected')}")
                return False
                
    except Exception as e:
        print(f"❌ Erro durante enrollment: {e}")
        return False


def verify_user(user_id: str, phrase: str, audio_path: str):
    """Verifica a identidade de um usuário"""
    print(f"🔐 Verificando identidade do usuário '{user_id}'...")
    
    audio_file = Path(audio_path)
    if not audio_file.exists():
        print(f"❌ Arquivo de áudio não encontrado: {audio_path}")
        return False
    
    try:
        with open(audio_path, 'rb') as audio:
            files = {'audio_file': ('audio.wav', audio, 'audio/wav')}
            data = {
                'user_id': user_id,
                'phrase_expected': phrase
            }
            response = requests.post(
                f"{BASE_URL}/voice/verify", 
                files=files, 
                data=data
            )
            
            result = response.json()
            
            if result.get('authenticated'):
                print("✅ AUTENTICADO!")
                print(f"   - Similaridade: {result.get('similarity', 0):.4f}")
                print(f"   - Threshold: {result.get('threshold', 0):.2f}")
                print(f"   - Transcrição: {result.get('transcription')}")
                return True
            else:
                print("❌ NÃO AUTENTICADO")
                print(f"   - Similaridade: {result.get('similarity', 0):.4f}")
                print(f"   - Threshold: {result.get('threshold', 0):.2f}")
                print(f"   - Mensagem: {result.get('message')}")
                if 'transcription' in result:
                    print(f"   - Transcrição: {result.get('transcription')}")
                return False
                
    except Exception as e:
        print(f"❌ Erro durante verificação: {e}")
        return False


def main():
    """Função principal"""
    print_separator()
    print("🎙️  TESTE DA API DE AUTENTICAÇÃO POR VOZ")
    print_separator()
    
    # 1. Verificar se API está online
    if not test_health():
        return
    
    print_separator()
    
    # 2. Obter frase de desafio
    phrase = get_challenge()
    if not phrase:
        return
    
    print_separator()
    
    # 3. Informações para o usuário
    print("📋 INSTRUÇÕES:")
    print(f"   1. Grave um áudio pronunciando: '{phrase}'")
    print("   2. Salve como 'test_audio.wav' nesta pasta")
    print("   3. O script fará o enrollment e depois a verificação")
    
    # Verificar se arquivo de teste existe
    audio_file = "test_audio.wav"
    if not Path(audio_file).exists():
        print(f"\n⚠️  Arquivo '{audio_file}' não encontrado!")
        print("   Crie um arquivo de áudio para continuar o teste.")
        print("\n   Você pode usar este comando para gravar (requer sounddevice):")
        print("   python -c \"import sounddevice as sd; import scipy.io.wavfile as wav; audio = sd.rec(int(3*16000), samplerate=16000, channels=1); sd.wait(); wav.write('test_audio.wav', 16000, audio)\"")
        return
    
    print_separator()
    
    # 4. Enrollment
    user_id = "test_user_123"
    if not enroll_user(user_id, phrase, audio_file):
        print("\n⚠️  Enrollment falhou. Verifique:")
        print("   - Se o áudio está claro")
        print("   - Se você pronunciou a frase correta")
        print("   - Se o formato do áudio é WAV")
        return
    
    print_separator()
    
    # 5. Aguardar um pouco
    print("⏳ Aguardando 2 segundos...")
    time.sleep(2)
    
    print_separator()
    
    # 6. Verificação (usando o mesmo áudio para teste)
    verify_user(user_id, phrase, audio_file)
    
    print_separator()
    
    # 7. Dicas finais
    print("💡 DICAS:")
    print("   - Para um teste real, grave áudios diferentes para enrollment e verificação")
    print("   - Use áudio de boa qualidade (sem ruído)")
    print("   - Fale claramente a frase completa")
    print("   - Formato ideal: WAV, 16kHz, mono")
    
    print_separator()
    
    print("✨ Teste concluído!")
    print("📚 Veja mais exemplos em EXAMPLES.md")
    print("📖 Documentação completa em README.md")
    print("🌐 API Docs: http://localhost:8000/docs")


if __name__ == "__main__":
    main()
