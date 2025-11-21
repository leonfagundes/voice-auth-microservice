"""
Teste completo da API com áudio sintético
Não precisa gravar áudio - funciona automaticamente!
"""
import requests
import numpy as np
import wave
import tempfile
import os
import time

BASE_URL = "http://localhost:8000"


def criar_audio_sintetico(frase, arquivo="audio_sintetico.wav"):
    """
    Cria um arquivo de áudio sintético (tom de 440Hz)
    Útil para testes automatizados
    """
    print(f"🎵 Criando áudio sintético...")
    
    sample_rate = 16000
    duracao = 2.0
    frequencia = 440.0  # Lá musical (A4)
    
    # Gerar onda senoidal
    t = np.linspace(0, duracao, int(sample_rate * duracao))
    audio_data = (np.sin(2 * np.pi * frequencia * t) * 32767 * 0.5).astype(np.int16)
    
    # Salvar como WAV
    with wave.open(arquivo, 'wb') as wf:
        wf.setnchannels(1)  # Mono
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(sample_rate)
        wf.writeframes(audio_data.tobytes())
    
    print(f"✅ Áudio criado: {arquivo}")
    print(f"   📊 Duração: {duracao}s")
    print(f"   📊 Sample rate: {sample_rate}Hz")
    print(f"   🎵 Tom: {frequencia}Hz (Lá musical)")
    
    return arquivo


def testar_health():
    """Testa se API está online"""
    print("\n1️⃣  Testando conexão com a API...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ API está online e funcionando!")
            print(f"   {response.json()}")
            return True
        else:
            print(f"❌ API retornou status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")
        print("\n⚠️  Inicie a API com: python start_api.py")
        return False


def obter_challenge():
    """Obtém frase de desafio"""
    print("\n2️⃣  Obtendo frase de desafio...")
    try:
        response = requests.get(f"{BASE_URL}/voice/challenge")
        response.raise_for_status()
        phrase = response.json()["phrase"]
        print(f"✅ Frase obtida: '{phrase}'")
        return phrase
    except Exception as e:
        print(f"❌ Erro: {e}")
        return None


def testar_enrollment(user_id, phrase, audio_file):
    """Testa enrollment"""
    print(f"\n3️⃣  Testando ENROLLMENT (usuário: {user_id})...")
    
    try:
        with open(audio_file, 'rb') as audio:
            files = {'audio_file': (audio_file, audio, 'audio/wav')}
            data = {
                'user_id': user_id,
                'phrase_expected': phrase
            }
            response = requests.post(
                f"{BASE_URL}/voice/enroll", 
                files=files, 
                data=data,
                timeout=30
            )
            
            result = response.json()
            
            print(f"\n📋 Resposta do Enrollment:")
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                if result.get('success'):
                    print(f"   ✅ Sucesso: {result.get('message')}")
                    print(f"   📝 User ID: {result.get('user_id')}")
                    print(f"   🗣️  Transcrição: {result.get('transcription')}")
                    return True
                else:
                    print(f"   ❌ Falha: {result.get('message')}")
            else:
                print(f"   ❌ Erro: {result.get('detail', result.get('message'))}")
            
            if 'transcription' in result:
                print(f"   🗣️  Transcrito: '{result['transcription']}'")
                if 'expected' in result:
                    print(f"   📢 Esperado: '{result['expected']}'")
            
            return False
            
    except Exception as e:
        print(f"❌ Erro durante enrollment: {e}")
        import traceback
        traceback.print_exc()
        return False


def testar_verificacao(user_id, phrase, audio_file):
    """Testa verificação"""
    print(f"\n4️⃣  Testando VERIFICAÇÃO (usuário: {user_id})...")
    
    try:
        with open(audio_file, 'rb') as audio:
            files = {'audio_file': (audio_file, audio, 'audio/wav')}
            data = {
                'user_id': user_id,
                'phrase_expected': phrase
            }
            response = requests.post(
                f"{BASE_URL}/voice/verify", 
                files=files, 
                data=data,
                timeout=30
            )
            
            result = response.json()
            
            print(f"\n📋 Resposta da Verificação:")
            print(f"   Status: {response.status_code}")
            
            if result.get('authenticated'):
                print(f"   🎉 AUTENTICADO!")
                print(f"   ✅ Similaridade: {result.get('similarity', 0):.4f} ({result.get('similarity', 0)*100:.1f}%)")
                print(f"   📊 Threshold: {result.get('threshold', 0):.2f} ({result.get('threshold', 0)*100:.0f}%)")
                print(f"   💬 {result.get('message')}")
            else:
                print(f"   ❌ NÃO AUTENTICADO")
                print(f"   📊 Similaridade: {result.get('similarity', 0):.4f} ({result.get('similarity', 0)*100:.1f}%)")
                print(f"   📊 Threshold necessário: {result.get('threshold', 0):.2f} ({result.get('threshold', 0)*100:.0f}%)")
                print(f"   💬 {result.get('message')}")
            
            if 'transcription' in result:
                print(f"   🗣️  Transcrição: '{result['transcription']}'")
            
            return result.get('authenticated', False)
            
    except Exception as e:
        print(f"❌ Erro durante verificação: {e}")
        return False


def main():
    """Função principal"""
    print("=" * 70)
    print("🧪 TESTE COMPLETO DA API - COM ÁUDIO SINTÉTICO")
    print("=" * 70)
    print("\nℹ️  Este teste usa áudio sintético (tom de 440Hz)")
    print("ℹ️  Não precisa gravar áudio - é totalmente automatizado!")
    print("\n⚠️  NOTA: O Vosk pode não transcrever áudio sintético corretamente")
    print("   mas serve para testar se a API está funcionando.")
    
    # 1. Testar conexão
    if not testar_health():
        return
    
    # 2. Obter frase
    phrase = obter_challenge()
    if not phrase:
        return
    
    # 3. Criar áudio sintético
    print(f"\n📢 Frase esperada: '{phrase}'")
    audio_file = criar_audio_sintetico(phrase)
    
    # 4. Testar enrollment
    user_id = f"test_user_{int(time.time())}"
    
    print("\n" + "=" * 70)
    print("🔄 INICIANDO TESTES...")
    print("=" * 70)
    
    enrollment_ok = testar_enrollment(user_id, phrase, audio_file)
    
    if not enrollment_ok:
        print("\n⚠️  Enrollment falhou (esperado com áudio sintético)")
        print("\n💡 PRÓXIMOS PASSOS:")
        print("   1. Use 'gravar_audio.py' para teste com áudio real")
        print("   2. Ou teste manualmente em: http://localhost:8000/docs")
        print("   3. Ou use Postman/cURL com arquivo de áudio real")
    else:
        # 5. Aguardar
        print("\n⏳ Aguardando 1 segundo...")
        time.sleep(1)
        
        # 6. Testar verificação
        verificacao_ok = testar_verificacao(user_id, phrase, audio_file)
    
    # 7. Limpar
    if os.path.exists(audio_file):
        os.unlink(audio_file)
        print(f"\n🧹 Arquivo temporário removido")
    
    # 8. Resumo
    print("\n" + "=" * 70)
    print("📊 RESUMO DO TESTE")
    print("=" * 70)
    print(f"   ✅ API online: Sim")
    print(f"   ✅ Challenge: Ok")
    print(f"   {'✅' if enrollment_ok else '⚠️ '} Enrollment: {'Sucesso' if enrollment_ok else 'Falhou (esperado com áudio sintético)'}")
    if enrollment_ok:
        print(f"   {'✅' if verificacao_ok else '❌'} Verificação: {'Autenticado' if verificacao_ok else 'Não autenticado'}")
    
    print("\n💡 COMO TESTAR COM ÁUDIO REAL:")
    print("   Opção 1: python gravar_audio.py")
    print("   Opção 2: http://localhost:8000/docs (Swagger UI)")
    print("   Opção 3: python test_api.py (com arquivo test_audio.wav)")
    print("   Opção 4: Veja TESTES_SEM_APP.md para mais opções")
    
    print("\n✨ Teste automatizado concluído!\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Teste cancelado")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
