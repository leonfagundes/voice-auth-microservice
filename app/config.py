"""
Configurações da aplicação
"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Configurações gerais da aplicação"""
    
    db_host: str = "localhost"
    db_port: int = 3306
    db_user: str = "root"
    db_password: str = "rootpassword"
    db_name: str = "auth_voice_db"
    
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    debug: bool = True
    
    similarity_threshold: float = 0.75
    vosk_model_path: str = "./models/vosk-model-small-pt-0.3"
    speechbrain_model: str = "speechbrain/spkrec-ecapa-voxceleb"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

    @property
    def database_url(self) -> str:
        """Retorna a URL de conexão do banco de dados"""
        return f"mysql+pymysql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
