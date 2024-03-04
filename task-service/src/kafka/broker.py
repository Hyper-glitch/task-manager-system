from faststream.kafka import KafkaBroker

from src.config import settings

broker = KafkaBroker(bootstrap_servers=settings.bootstrap_servers)
