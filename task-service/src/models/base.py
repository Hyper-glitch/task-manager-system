from sqlalchemy.orm import declarative_base, registry

mapper_registry = registry()
Base = declarative_base()
