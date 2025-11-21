"""
Utilidades para processamento de áudio
"""
import os
import json
import logging
import tempfile
import wave
import warnings
import shutil
import numpy as np
from typing import Tuple, Optional
from vosk import Model, KaldiRecognizer

# Suprimir warnings do torchaudio
warnings.filterwarnings("ignore", message="torchaudio._backend.set_audio_backend has been deprecated")
warnings.filterwarnings("ignore", message="torchvision is not available")

import torch
import torchaudio
from speechbrain.inference.speaker import EncoderClassifier

logger = logging.getLogger(__name__)

_vosk_model = None
_speechbrain_model = None
_symlink_patched = False


def get_vosk_model(model_path: str) -> Model:
    """
    Retorna o modelo Vosk (cached)
    
    Args:
        model_path: Caminho para o modelo Vosk
        
    Returns:
        Modelo Vosk carregado
    """
    global _vosk_model
    
    if _vosk_model is None:
        logger.info(f"Carregando modelo Vosk de {model_path}")
        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"Modelo Vosk não encontrado em {model_path}. "
                "Baixe o modelo de https://alphacephei.com/vosk/models"
            )
        _vosk_model = Model(model_path)
        logger.info("Modelo Vosk carregado com sucesso")
    
    return _vosk_model


def _patch_symlink_for_windows():
    """
    Substitui os.symlink por shutil.copy2 no Windows para evitar erro de permissão
    Também patch na função fetch do SpeechBrain
    """
    global _symlink_patched
    
    if _symlink_patched:
        return
    
    import platform
    if platform.system() != "Windows":
        return
    
    logger.info("Aplicando patch para evitar symlinks no Windows")
    
    original_symlink = os.symlink
    
    def patched_symlink(src, dst, target_is_directory=False, dir_fd=None):
        """Copia arquivo em vez de criar symlink"""
        try:
            logger.info(f"Copiando (em vez de symlink): {src} -> {dst}")
            
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            
            shutil.copy2(src, dst)
        except Exception as e:
            logger.error(f"Erro ao copiar arquivo: {e}")
            raise
    
    os.symlink = patched_symlink
    
    try:
        from speechbrain.utils import fetching
        original_fetch = fetching.fetch
        
        def patched_fetch(filename, source, savedir, overwrite=False, save_filename=None, 
                         use_auth_token=False, revision=None, **kwargs):
            """Versão modificada que copia em vez de criar symlinks"""
            try:
                result = original_fetch(filename, source, savedir, overwrite, 
                                      save_filename, use_auth_token, revision, **kwargs)
            except OSError as e:
                if "privilege" in str(e).lower() or "1314" in str(e):
                    logger.warning(f"Erro de symlink detectado, copiando manualmente: {e}")
                    
                    from pathlib import Path
                    import huggingface_hub
                    
                    cache_dir = Path.home() / ".cache" / "huggingface" / "hub"
                    
                    try:
                        cached_file = huggingface_hub.hf_hub_download(
                            repo_id=source,
                            filename=filename,
                            cache_dir=cache_dir,
                            revision=revision,
                            use_auth_token=use_auth_token if use_auth_token else None
                        )
                        
                        dest_filename = save_filename if save_filename else filename
                        dest_path = Path(savedir) / dest_filename
                        dest_path.parent.mkdir(parents=True, exist_ok=True)
                        
                        shutil.copy2(cached_file, dest_path)
                        logger.info(f"Arquivo copiado com sucesso: {dest_path}")
                        
                        return str(dest_path)
                    except Exception as copy_error:
                        logger.error(f"Erro ao copiar arquivo: {copy_error}")
                        raise
                else:
                    raise
            
            return result
        
        fetching.fetch = patched_fetch
        logger.info("Patch de fetch do SpeechBrain aplicado")
    except Exception as e:
        logger.warning(f"Não foi possível aplicar patch no fetch: {e}")
    
    _symlink_patched = True
    logger.info("Patch de symlink aplicado com sucesso")


def get_speechbrain_model(model_name: str) -> EncoderClassifier:
    """
    Retorna o modelo SpeechBrain (cached)
    
    Args:
        model_name: Nome do modelo SpeechBrain
        
    Returns:
        Modelo SpeechBrain carregado
    """
    global _speechbrain_model
    
    if _speechbrain_model is None:
        logger.info(f"Carregando modelo SpeechBrain: {model_name}")
        
        _patch_symlink_for_windows()
        
        _speechbrain_model = EncoderClassifier.from_hparams(
            source=model_name,
            savedir="./models/speechbrain",
            run_opts={"device": "cpu"},
            use_auth_token=False
        )
        logger.info("Modelo SpeechBrain carregado com sucesso")
    
    return _speechbrain_model


def convert_to_wav(audio_bytes: bytes) -> Tuple[str, int]:
    """
    Converte bytes de áudio para arquivo WAV temporário
    
    Args:
        audio_bytes: Bytes do arquivo de áudio
        
    Returns:
        Tupla com (caminho do arquivo WAV, sample rate)
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
        temp_file.write(audio_bytes)
        temp_path = temp_file.name
    
    with wave.open(temp_path, 'rb') as wf:
        sample_rate = wf.getframerate()
    
    return temp_path, sample_rate


def transcribe_audio(audio_bytes: bytes, vosk_model_path: str) -> Optional[str]:
    """
    Transcreve áudio usando Vosk
    
    Args:
        audio_bytes: Bytes do arquivo de áudio (WAV)
        vosk_model_path: Caminho para o modelo Vosk
        
    Returns:
        Texto transcrito ou None se falhar
    """
    try:
        wav_path, sample_rate = convert_to_wav(audio_bytes)
        
        model = get_vosk_model(vosk_model_path)
        
        recognizer = KaldiRecognizer(model, sample_rate)
        recognizer.SetWords(True)
        
        with wave.open(wav_path, 'rb') as wf:
            while True:
                data = wf.readframes(4000)
                if len(data) == 0:
                    break
                recognizer.AcceptWaveform(data)
        
        result = json.loads(recognizer.FinalResult())
        transcription = result.get('text', '').strip()
        
        os.unlink(wav_path)
        
        logger.info(f"Transcrição: {transcription}")
        return transcription if transcription else None
        
    except Exception as e:
        logger.error(f"Erro ao transcrever áudio: {e}")
        if 'wav_path' in locals():
            try:
                os.unlink(wav_path)
            except:
                pass
        return None


def extract_voice_embedding(audio_bytes: bytes, speechbrain_model_name: str) -> Optional[list]:
    """
    Extrai embedding de voz usando SpeechBrain
    
    Args:
        audio_bytes: Bytes do arquivo de áudio
        speechbrain_model_name: Nome do modelo SpeechBrain
        
    Returns:
        Lista com o embedding ou None se falhar
    """
    try:
        wav_path, sample_rate = convert_to_wav(audio_bytes)
        
        model = get_speechbrain_model(speechbrain_model_name)
        
        waveform, sr = torchaudio.load(wav_path)
        
        if waveform.shape[0] > 1:
            waveform = torch.mean(waveform, dim=0, keepdim=True)
        
        if sr != 16000:
            resampler = torchaudio.transforms.Resample(sr, 16000)
            waveform = resampler(waveform)
        
        embedding = model.encode_batch(waveform)
        embedding_array = embedding.squeeze().cpu().numpy()
        
        os.unlink(wav_path)
        
        logger.info(f"Embedding extraído com dimensão: {embedding_array.shape}")
        return embedding_array.tolist()
        
    except Exception as e:
        logger.error(f"Erro ao extrair embedding: {e}", exc_info=True)
        if 'wav_path' in locals():
            try:
                os.unlink(wav_path)
            except:
                pass
        return None


def validate_transcription(transcription: str, expected_phrase: str, threshold: float = 0.5) -> bool:
    """
    Valida se a transcrição corresponde à frase esperada
    
    Args:
        transcription: Texto transcrito
        expected_phrase: Frase esperada
        threshold: Limiar de similaridade (0-1) - padrão 0.5 (50%)
        
    Returns:
        True se a transcrição é válida
    """
    if not transcription or not expected_phrase:
        return False
    
    trans_normalized = transcription.lower().strip()
    expected_normalized = expected_phrase.lower().strip()
    
    if trans_normalized == expected_normalized:
        logger.info(f"Similaridade de transcrição: 1.00 (correspondência exata)")
        return True
    
    trans_words = set(trans_normalized.split())
    expected_words = set(expected_normalized.split())
    
    if len(expected_words) == 0:
        return False
    
    intersection = len(trans_words.intersection(expected_words))
    union = len(trans_words.union(expected_words))
    
    similarity = intersection / union if union > 0 else 0
    
    logger.info(f"Similaridade de transcrição: {similarity:.2f} (threshold: {threshold})")
    
    if similarity < threshold:
        logger.warning(f"❌ Transcrição rejeitada - Esperado: '{expected_normalized}'")
        logger.warning(f"❌ Transcrição rejeitada - Recebido: '{trans_normalized}'")
    
    return similarity >= threshold
