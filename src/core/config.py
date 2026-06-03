from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "PropTech Booking SaaS"
    API_V1_STR: str = "/api/v1"
    
    # Database (asyncpg)
    POSTGRES_USER: str = "admin"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "proptech_saas"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432

    @property
    def database_url(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Security
    SECRET_KEY: str = "SUPER_SECRET_KEY_CHANGE_ME"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # S3 (MinIO)
    S3_ENDPOINT_URL: str = "http://localhost:9000"
    S3_ACCESS_KEY: str = "minioadmin"
    S3_SECRET_KEY: str = "miniopassword"
    S3_BUCKET_NAME: str = "property-images"

    # Telegram notifications
    TELEGRAM_BOT_TOKEN: str = "8972361768:AAEaWf1gpXMPYWFnBuJ5OBBApzDZWjmh6Bo"
    TELEGRAM_CHAT_ID: str = "848484880"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

settings = Settings()
