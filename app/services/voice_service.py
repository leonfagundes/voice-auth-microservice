"""
Serviço de autenticação por voz
"""
import logging
import random
from typing import Optional, Dict, Any, Tuple
from sqlalchemy.orm import Session
from app.repositories.voice_repository import VoiceRepository
from app.utils.audio_processing import (
    transcribe_audio,
    extract_voice_embedding,
    validate_transcription
)
from app.utils.similarity import calculate_cosine_similarity
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

CHALLENGE_PHRASES = [
    "Eu autorizo o acesso ao sistema através da minha biometria vocal única e intransferível para garantir a máxima segurança",
    "Confirmo minha identidade utilizando as características únicas da minha voz para autenticação segura no sistema de proteção avançada",
    "Reconheço que minha voz possui padrões únicos e autorizo o sistema a verificar minha identidade através desta tecnologia biométrica",
    "Declaro que estou fornecendo voluntariamente minha amostra vocal para cadastro no sistema de autenticação por biometria de voz",
    "Esta é minha voz natural e autorizo sua utilização como método de identificação pessoal em todos os acessos ao sistema",
    "Confirmo que as características da minha voz são únicas e podem ser utilizadas como forma de autenticação biométrica segura",
    "Eu compreendo que minha voz será analisada e comparada com padrões previamente cadastrados para verificação de identidade",
    "Autorizo o processamento das características vocais da minha voz para fins de autenticação e controle de acesso ao sistema",
    "Reconheço minha voz como uma credencial biométrica única e autorizo seu uso para verificação de identidade no sistema",
    "Esta declaração vocal confirma minha identidade e autoriza o acesso utilizando tecnologia de reconhecimento de locutor avançada"
]


class VoiceService:
    """Serviço para lógica de negócio de autenticação por voz"""
    
    def __init__(self, db: Session):
        self.db = db
        self.repository = VoiceRepository(db)
    
    def get_challenge_phrase(self) -> str:
        """
        Retorna uma frase aleatória para desafio de voz
        
        Returns:
            Frase aleatória
        """
        return random.choice(CHALLENGE_PHRASES)
    
    def enroll_user(
        self,
        user_id: str,
        audio_bytes: bytes,
        expected_phrase: str
    ) -> Dict[str, Any]:
        """
        Realiza o enrollment (cadastro) de voz de um usuário
        
        Args:
            user_id: ID do usuário
            audio_bytes: Bytes do arquivo de áudio
            expected_phrase: Frase esperada
            
        Returns:
            Dicionário com resultado do enrollment
        """
        logger.info(f"Iniciando enrollment para usuário {user_id}")
        
        transcription = transcribe_audio(audio_bytes, settings.vosk_model_path)
        if not transcription:
            return {
                "success": False,
                "message": "Não foi possível transcrever o áudio"
            }
        
        is_valid = validate_transcription(transcription, expected_phrase)
        if not is_valid:
            return {
                "success": False,
                "message": "A frase pronunciada não corresponde à esperada",
                "transcription": transcription,
                "expected": expected_phrase
            }
        
        embedding = extract_voice_embedding(audio_bytes, settings.speechbrain_model)
        if not embedding:
            return {
                "success": False,
                "message": "Não foi possível extrair características da voz"
            }
        
        existing_profile = self.repository.get_profile_by_user_id(user_id)
        
        if existing_profile:
            profile = self.repository.update_profile(user_id, embedding)
        else:
            profile = self.repository.create_profile(user_id, embedding)
        
        if not profile:
            return {
                "success": False,
                "message": "Erro ao salvar perfil de voz no banco de dados"
            }
        
        logger.info(f"Enrollment concluído com sucesso para usuário {user_id}")
        return {
            "success": True,
            "message": "Perfil de voz cadastrado com sucesso",
            "user_id": user_id,
            "transcription": transcription
        }
    
    def verify_user(
        self,
        user_id: str,
        audio_bytes: bytes,
        expected_phrase: str
    ) -> Dict[str, Any]:
        """
        Verifica a identidade de um usuário através da voz
        
        Args:
            user_id: ID do usuário
            audio_bytes: Bytes do arquivo de áudio
            expected_phrase: Frase esperada
            
        Returns:
            Dicionário com resultado da verificação
        """
        logger.info(f"Iniciando verificação para usuário {user_id}")
        
        profile = self.repository.get_profile_by_user_id(user_id)
        if not profile:
            return {
                "authenticated": False,
                "message": "Usuário não possui perfil de voz cadastrado"
            }
        
        transcription = transcribe_audio(audio_bytes, settings.vosk_model_path)
        if not transcription:
            return {
                "authenticated": False,
                "message": "Não foi possível transcrever o áudio"
            }
        
        is_valid = validate_transcription(transcription, expected_phrase)
        if not is_valid:
            return {
                "authenticated": False,
                "message": "A frase pronunciada não corresponde à esperada",
                "transcription": transcription,
                "expected": expected_phrase
            }
        
        current_embedding = extract_voice_embedding(audio_bytes, settings.speechbrain_model)
        if not current_embedding:
            return {
                "authenticated": False,
                "message": "Não foi possível extrair características da voz"
            }
        
        stored_embedding = profile.embedding
        similarity = calculate_cosine_similarity(current_embedding, stored_embedding)
        
        authenticated = similarity >= settings.similarity_threshold
        
        logger.info(
            f"Verificação para usuário {user_id}: "
            f"similaridade={similarity:.4f}, "
            f"autenticado={authenticated}"
        )
        
        return {
            "authenticated": authenticated,
            "similarity": float(similarity),
            "threshold": settings.similarity_threshold,
            "message": "Autenticação bem-sucedida" if authenticated else "Voz não reconhecida",
            "transcription": transcription
        }
    
    def load_phrases_from_file(self, filepath: str) -> bool:
        """
        Carrega frases de desafio de um arquivo
        
        Args:
            filepath: Caminho para arquivo de frases
            
        Returns:
            True se carregado com sucesso
        """
        global CHALLENGE_PHRASES
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                phrases = [line.strip() for line in f if line.strip()]
                if phrases:
                    CHALLENGE_PHRASES = phrases
                    logger.info(f"{len(phrases)} frases carregadas de {filepath}")
                    return True
            return False
        except Exception as e:
            logger.error(f"Erro ao carregar frases de {filepath}: {e}")
            return False
