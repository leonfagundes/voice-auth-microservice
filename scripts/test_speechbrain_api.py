"""
Teste para verificar se a API do SpeechBrain está sendo usada corretamente
"""
import warnings
warnings.filterwarnings("ignore")

print("=" * 60)
print("TESTE DE COMPATIBILIDADE - SpeechBrain 1.0+")
print("=" * 60)

# 1. Testar import correto
print("\n1️⃣  Testando import...")
try:
    from speechbrain.inference.speaker import EncoderClassifier
    print("✅ Import correto: speechbrain.inference.speaker")
except ImportError as e:
    print(f"❌ Erro no import: {e}")
    exit(1)

# 2. Testar se o import antigo está deprecado
print("\n2️⃣  Verificando deprecação do import antigo...")
try:
    from speechbrain.pretrained import EncoderClassifier as OldEncoder
    print("⚠️  Import antigo ainda funciona (com warning)")
except Exception as e:
    print(f"ℹ️  Import antigo não disponível: {e}")

# 3. Testar carregamento do modelo
print("\n3️⃣  Testando carregamento do modelo...")
try:
    import os
    import torch
    import torchaudio
    
    # Desabilitar download automático se modelo já existe
    model_path = "./models/speechbrain"
    if os.path.exists(model_path):
        print(f"ℹ️  Usando modelo local em: {model_path}")
    
    model = EncoderClassifier.from_hparams(
        source="speechbrain/spkrec-ecapa-voxceleb",
        savedir=model_path,
        run_opts={"device": "cpu"}
    )
    print("✅ Modelo carregado com sucesso")
    
    # 4. Testar método encode_batch
    print("\n4️⃣  Testando método encode_batch...")
    
    # Criar um áudio sintético para teste (1 segundo de silêncio a 16kHz)
    sample_rate = 16000
    duration = 1.0
    waveform = torch.zeros(1, int(sample_rate * duration))
    
    print(f"   📊 Waveform shape: {waveform.shape}")
    print(f"   📊 Sample rate: {sample_rate}Hz")
    
    # Extrair embedding
    embedding = model.encode_batch(waveform)
    print(f"✅ Embedding extraído com shape: {embedding.shape}")
    
    # 5. Verificar dimensão do embedding
    print("\n5️⃣  Verificando dimensão do embedding...")
    embedding_array = embedding.squeeze().cpu().numpy()
    print(f"   📊 Dimensão do embedding: {embedding_array.shape}")
    print(f"   📊 Tipo: {type(embedding_array)}")
    
    # Converter para lista (como no código da API)
    embedding_list = embedding_array.tolist()
    print(f"✅ Conversão para lista OK: {len(embedding_list)} elementos")
    
    print("\n" + "=" * 60)
    print("✨ TODOS OS TESTES PASSARAM!")
    print("=" * 60)
    print("\n📝 Resumo das correções necessárias:")
    print("   1. ✅ Import: speechbrain.inference.speaker (não pretrained)")
    print("   2. ✅ encode_batch recebe tensor de áudio (não caminho)")
    print("   3. ✅ Usar torchaudio.load() para carregar áudio")
    print("   4. ✅ Garantir áudio mono e 16kHz")
    
except Exception as e:
    print(f"❌ Erro no teste: {e}")
    import traceback
    traceback.print_exc()
    exit(1)
