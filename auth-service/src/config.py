from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_host: str
    api_port: int
    sqlalchemy_database_uri: str

    class Config:
        env_file = ".env"


settings = Settings()
