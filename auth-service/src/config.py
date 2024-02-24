from pydantic import Field
from pydantic_settings import BaseSettings

from src.conf.amqp import AMQPConfigSettings
from src.enums.producer import UserProducer


class Settings(BaseSettings):
    project: str = UserProducer.AUTH_SERVICE.value
    api_host: str
    api_port: int
    database_dsn: str
    kafka: AMQPConfigSettings = Field(default_factory=AMQPConfigSettings)

    class Config:
        env_file = ".env"


settings = Settings()
