import uuid

from sqlalchemy import Enum
from sqlalchemy.dialects.postgresql import UUID

from src.database import db
from src.models.base import Base


class User(Base):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(UUID(as_uuid=True), nullable=False, default=uuid.uuid4)
    role = db.Column(
        Enum(UserRoles),
        nullable=False,
        default=UserRoles.EMPLOYEE,
        server_default=db.text(f"'{UserRoles.EMPLOYEE.value}'"),
    )
    username = db.Column(db.String(128), nullable=False, default="", server_default=db.text("''"))
    email = db.Column(db.String(128), nullable=False, default="", server_default=db.text("''"))
    is_deleted = db.Column(db.Boolean)
