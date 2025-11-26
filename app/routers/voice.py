"""
Rotas da API de autenticação por voz
"""
import logging
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.services.voice_service import VoiceService
from app.repositories.voice_repository import VoiceRepository

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/voice", tags=["voice"])


class ChallengeResponse(BaseModel):
    """Response para endpoint de desafio"""
    phrase: str


class EnrollResponse(BaseModel):
    """Response para endpoint de enrollment"""
    success: bool
    message: str
    user_id: str = None
    transcription: str = None


class VerifyResponse(BaseModel):
    """Response para endpoint de verificação"""
    authenticated: bool
    similarity: float = None
    threshold: float = None
    message: str
    transcription: str = None


class UserExistsResponse(BaseModel):
    """Response para endpoint de verificação de existência de usuário"""
    exists: bool
    user_id: str


@router.get("/challenge", response_model=ChallengeResponse)
async def get_challenge(db: Session = Depends(get_db)):
    """
    GET /voice/challenge
    
    Retorna uma frase aleatória para o usuário pronunciar
    """
    try:
        service = VoiceService(db)
        phrase = service.get_challenge_phrase()
        
        logger.info(f"Frase de desafio gerada: {phrase}")
        
        return ChallengeResponse(phrase=phrase)
    
    except Exception as e:
        logger.error(f"Erro ao gerar frase de desafio: {e}")
        raise HTTPException(status_code=500, detail="Erro ao gerar frase de desafio")


@router.post("/enroll", response_model=EnrollResponse)
async def enroll_voice(
    user_id: str = Form(...),
    phrase_expected: str = Form(...),
    audio_file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    POST /voice/enroll
    
    Realiza o enrollment (cadastro) de voz de um usuário
    
    Args:
        user_id: ID único do usuário
        phrase_expected: Frase que deveria ter sido pronunciada
        audio_file: Arquivo de áudio (WAV recomendado)
    """
    try:
        # Validar formato do arquivo
        if not audio_file.content_type or 'audio' not in audio_file.content_type:
            raise HTTPException(
                status_code=400,
                detail="Formato de arquivo inválido. Envie um arquivo de áudio."
            )
        
        # Ler bytes do arquivo
        audio_bytes = await audio_file.read()
        
        if len(audio_bytes) == 0:
            raise HTTPException(
                status_code=400,
                detail="Arquivo de áudio vazio"
            )
        
        service = VoiceService(db)
        result = service.enroll_user(user_id, audio_bytes, phrase_expected)
        
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["message"])
        
        return EnrollResponse(**result)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro no enrollment: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao processar enrollment: {str(e)}")


@router.get("/user/{user_id}/exists", response_model=UserExistsResponse)
async def check_user_exists(
    user_id: str,
    db: Session = Depends(get_db)
):
    """
    GET /voice/user/{user_id}/exists
    
    Verifica se existe um perfil de voz cadastrado para o user_id fornecido
    
    Args:
        user_id: ID único do usuário
        
    Returns:
        UserExistsResponse com exists=True se o usuário existe, False caso contrário
    """
    try:
        repository = VoiceRepository(db)
        exists = repository.user_exists(user_id)
        
        logger.info(f"Verificação de existência para user_id {user_id}: {exists}")
        
        return UserExistsResponse(exists=exists, user_id=user_id)
    
    except Exception as e:
        logger.error(f"Erro ao verificar existência do usuário {user_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao verificar existência do usuário: {str(e)}"
        )


@router.post("/verify", response_model=VerifyResponse)
async def verify_voice(
    user_id: str = Form(...),
    phrase_expected: str = Form(...),
    audio_file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    POST /voice/verify
    
    Verifica a identidade de um usuário através da voz
    
    Args:
        user_id: ID único do usuário
        phrase_expected: Frase que deveria ter sido pronunciada
        audio_file: Arquivo de áudio (WAV recomendado)
    """
    try:
        if not audio_file.content_type or 'audio' not in audio_file.content_type:
            raise HTTPException(
                status_code=400,
                detail="Formato de arquivo inválido. Envie um arquivo de áudio."
            )
        
        audio_bytes = await audio_file.read()
        
        if len(audio_bytes) == 0:
            raise HTTPException(
                status_code=400,
                detail="Arquivo de áudio vazio"
            )
        
        service = VoiceService(db)
        result = service.verify_user(user_id, audio_bytes, phrase_expected)
        
        return VerifyResponse(**result)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro na verificação: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao processar verificação: {str(e)}")
