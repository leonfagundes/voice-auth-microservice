"""Script para gravar áudio e testar a API automaticamente"""
import requests
import numpy as np
import wave
import time

BASE_URL = "http://localhost:8000"

def gravar_audio(duracao=3, sample_rate=16000, arquivo="gravacao.wav"):
    """Grava áudio usando sounddevice"""
    print(f"\n🎙️ Preparando para gravar {duracao} segundos...")
    
    try:
        import sounddevice as sd
        
        print("\n" + "="*60)
        print("🔴 GRAVANDO EM 3 SEGUNDOS...")
        print("="*60)
        time.sleep(1)
        print("3...")
        time.sleep(1)
        print("2...")
        time.sleep(1)
        print("1...")
        time.sleep(1)
        print("\n🔴 GRAVANDO! Fale agora...")
        
        # Gravar áudio
        audio = sd.rec(
            int(duracao * sample_rate), 
            samplerate=sample_rate, 
            channels=1,
            dtype='int16'
        )
        sd.wait()
        
        print("✅ Gravação concluída!")
        
        # Salvar como WAV
        with wave.open(arquivo, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)  # 16-bit
            wf.setframerate(sample_rate)
            wf.writeframes(audio.tobytes())
        
        print(f"💾 Áudio salvo em: {arquivo}")
        return arquivo
        
    except ImportError:
        print("❌ Biblioteca 'sounddevice' não instalada!")
        print("\nInstale com:")
        print("   pip install sounddevice")
        return None
    except Exception as e:
        print(f"❌ Erro ao gravar: {e}")
        return None


def main():
    """Função principal"""
    print("="*70)
    print("🎙️  TESTE DE VOZ - GRAVAÇÃO E AUTENTICAÇÃO")
    print("="*70)
    
    print("\n1️⃣  Verificando API...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ API está online!")
        else:
            print(f"❌ API retornou status {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Erro: {e}")
        print("\n⚠️  Certifique-se de que a API está rodando:")
        print("   python start_api.py")
        return
    
    print("\n2️⃣  Obtendo frase de desafio...")
    try:
        response = requests.get(f"{BASE_URL}/voice/challenge")
        phrase = response.json()["phrase"]
        print(f"✅ Frase: '{phrase}'")
    except Exception as e:
        print(f"❌ Erro ao obter frase: {e}")
        return
    
    print("\n" + "="*70)
    print("📋 INSTRUÇÕES:")
    print(f"   Você vai gravar 3 segundos de áudio")
    print(f"   Fale claramente esta frase:")
    print(f"\n   📢 '{phrase}'")
    print("="*70)
    
    input("\n⏸️  Pressione ENTER quando estiver pronto para gravar...")
    
    # 4. Gravar áudio
    arquivo_audio = gravar_audio(duracao=3)
    if not arquivo_audio:
        return
    
    # 5. Enrollment
    print("\n3️⃣  Fazendo enrollment...")
    user_id = f"usuario_{int(time.time())}"
    
    try:
        with open(arquivo_audio, 'rb') as audio:
            files = {'audio_file': (arquivo_audio, audio, 'audio/wav')}
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
                print(f"   📝 User ID: {user_id}")
                print(f"   🗣️  Transcrição: {result.get('transcription')}")
            else:
                print(f"❌ Falha no enrollment: {result.get('message')}")
                if 'transcription' in result:
                    print(f"   🗣️  O que ouvimos: '{result['transcription']}'")
                    print(f"   📢 Esperávamos: '{phrase}'")
                return
                
    except Exception as e:
        print(f"❌ Erro: {e}")
        return
    
    # 6. Aguardar
    print("\n⏳ Aguardando 2 segundos...")
    time.sleep(2)
    
    # 7. Verificação
    print("\n4️⃣  Testando verificação (usando mesmo áudio)...")
    
    try:
        with open(arquivo_audio, 'rb') as audio:
            files = {'audio_file': (arquivo_audio, audio, 'audio/wav')}
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
            
            print("\n" + "="*70)
            if result.get('authenticated'):
                print("🎉 AUTENTICADO COM SUCESSO!")
                print("="*70)
                print(f"   ✅ Similaridade: {result.get('similarity', 0):.2%}")
                print(f"   📊 Threshold: {result.get('threshold', 0):.2%}")
                print(f"   🗣️  Transcrição: {result.get('transcription')}")
            else:
                print("❌ NÃO AUTENTICADO")
                print("="*70)
                print(f"   Similaridade: {result.get('similarity', 0):.2%}")
                print(f"   Threshold necessário: {result.get('threshold', 0):.2%}")
                print(f"   Mensagem: {result.get('message')}")
            print("="*70)
                
    except Exception as e:
        print(f"❌ Erro: {e}")
        return
    
    # 8. Dicas finais
    print("\n💡 PRÓXIMOS PASSOS:")
    print("   1. Grave outro áudio diferente para testar verificação real")
    print("   2. Teste com diferentes usuários")
    print("   3. Veja a documentação: http://localhost:8000/docs")
    print(f"   4. Seu áudio está salvo em: {arquivo_audio}")
    
    print("\n✨ Teste concluído!\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Teste cancelado pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        import traceback
        traceback.print_exc()
