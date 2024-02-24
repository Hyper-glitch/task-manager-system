from src.app import app
from src.config import settings

if __name__ == "__main__":
    app.run(host=settings.api_host, port=settings.api_port)
