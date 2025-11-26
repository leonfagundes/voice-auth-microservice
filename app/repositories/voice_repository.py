"""
Repository para acesso aos dados de perfis de voz
"""
import logging
from typing import Optional
from sqlalchemy.orm import Session
from app.models.user_voice_profile import UserVoiceProfile

logger = logging.getLogger(__name__)


class VoiceRepository:
    """Repository para operações de banco de dados relacionadas a perfis de voz"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_profile_by_user_id(self, user_id: str) -> Optional[UserVoiceProfile]:
        """
        Busca perfil de voz por user_id
        
        Args:
            user_id: ID do usuário
            
        Returns:
            UserVoiceProfile ou None se não encontrado
        """
        try:
            profile = self.db.query(UserVoiceProfile).filter(
                UserVoiceProfile.user_id == user_id
            ).first()
            return profile
        except Exception as e:
            logger.error(f"Erro ao buscar perfil do usuário {user_id}: {e}")
            return None
    
    def create_profile(self, user_id: str, embedding: list) -> Optional[UserVoiceProfile]:
        """
        Cria um novo perfil de voz
        
        Args:
            user_id: ID do usuário
            embedding: Vetor de embedding
            
        Returns:
            UserVoiceProfile criado ou None se falhar
        """
        try:
            profile = UserVoiceProfile(
                user_id=user_id,
                embedding=embedding
            )
            self.db.add(profile)
            self.db.commit()
            self.db.refresh(profile)
            logger.info(f"Perfil de voz criado para usuário {user_id}")
            return profile
        except Exception as e:
            logger.error(f"Erro ao criar perfil para usuário {user_id}: {e}")
            self.db.rollback()
            return None
    
    def update_profile(self, user_id: str, embedding: list) -> Optional[UserVoiceProfile]:
        """
        Atualiza perfil de voz existente
        
        Args:
            user_id: ID do usuário
            embedding: Novo vetor de embedding
            
        Returns:
            UserVoiceProfile atualizado ou None se falhar
        """
        try:
            profile = self.get_profile_by_user_id(user_id)
            if profile:
                profile.embedding = embedding
                self.db.commit()
                self.db.refresh(profile)
                logger.info(f"Perfil de voz atualizado para usuário {user_id}")
                return profile
            return None
        except Exception as e:
            logger.error(f"Erro ao atualizar perfil do usuário {user_id}: {e}")
            self.db.rollback()
            return None
    
    def delete_profile(self, user_id: str) -> bool:
        """
        Remove perfil de voz
        
        Args:
            user_id: ID do usuário
            
        Returns:
            True se removido com sucesso, False caso contrário
        """
        try:
            profile = self.get_profile_by_user_id(user_id)
            if profile:
                self.db.delete(profile)
                self.db.commit()
                logger.info(f"Perfil de voz removido para usuário {user_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"Erro ao remover perfil do usuário {user_id}: {e}")
            self.db.rollback()
            return False
    
    def user_exists(self, user_id: str) -> bool:
        """
        Verifica se existe um perfil de voz cadastrado para o user_id
        
        Args:
            user_id: ID do usuário
            
        Returns:
            True se o usuário existe, False caso contrário
        """
        try:
            exists = self.db.query(UserVoiceProfile).filter(
                UserVoiceProfile.user_id == user_id
            ).count() > 0
            return exists
        except Exception as e:
            logger.error(f"Erro ao verificar existência do usuário {user_id}: {e}")
            return False
