from pydantic_settings import BaseSettings


class BaseKafkaSettings(BaseSettings):
    host: str = "localhost"
    port: int = 9092
    business_command_topic: str = ""
    data_streaming_topic: str = ""
    error_topic: str = ""
    reconnect_waiting: int
    max_pool_interval_ms: int

    @property
    def bootstrap_servers(self) -> str:
        return f"{self.host}:{self.port}"
