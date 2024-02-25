from pydantic_settings import BaseSettings

from src.enums.producer import UserProducer


class Settings(BaseSettings):
    project: str = UserProducer.AUTH_SERVICE.value
    api_host: str
    api_port: int
    database_dsn: str

    kafka_host: str
    kafka_port: int
    business_event_topic: str
    data_streaming_topic: str
    error_topic: str
    reconnect_waiting: int
    max_pool_interval_ms: int
    group_id: str

    class Config:
        env_file = "../.env"

    @property
    def bootstrap_servers(self) -> str:
        return f"{self.kafka_host}:{self.kafka_port}"


settings = Settings()
