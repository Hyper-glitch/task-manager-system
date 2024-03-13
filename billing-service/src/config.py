from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    project: str = "billing-service"
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

    redis_host: str
    redis_port: int
    redis_db: int

    auth_code_expiration: int
    access_token_expiration: int
    refresh_token_expiration: int
    secret_key: str
    public_key: str
    token_algorithm: str = "RS256"

    class Config:
        env_file = ".env"

    @property
    def bootstrap_servers(self) -> str:
        return f"{self.kafka_host}:{self.kafka_port}"


settings = Settings()
