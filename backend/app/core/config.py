from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    app_name: str = "JobForge"
    app_env: str = "development"
    debug: bool = True
    secret_key: str
    access_token_expire_minutes: int = 60
    refresh_token_expire_days: int = 7

    database_url: str

    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    aws_region: str = "us-east-1"
    s3_bucket_name: str = "jobforge-resumes"

    anthropic_api_key: str

    allowed_origins: str = "http://localhost:3000,http://localhost:5173"

    @property
    def cors_origins(self) -> List[str]:
        return [origin.strip() for origin in self.allowed_origins.split(",")]

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()