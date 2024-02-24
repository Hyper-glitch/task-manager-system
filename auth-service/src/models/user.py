import uuid
from datetime import datetime

from sqlalchemy import Enum, DateTime
from sqlalchemy.dialects.postgresql import UUID

from src.database import db
from src.enums.roles import UserRoles


class User(db.Model):
    __table__ = "user"

    username = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False, unique=True)
    beak_shape = db.Column(db.String(128), nullable=False, unique=True)
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(UUID(as_uuid=True), nullable=False, default=uuid.uuid4)
    role = db.Column(
        Enum(UserRoles),
        nullable=False,
        default=UserRoles.EMPLOYEE,
        server_default=db.text(f"'{UserRoles.EMPLOYEE.value}'"),
    )


class UserRefreshToken:
    __table__ = "user_refresh_token"

    user_id = db.Column("user_id", db.ForeignKey("user.id"), unique=True),
    refresh_token = db.Column("refresh_token", db.Text, nullable=False),
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(
        "created_at",
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        server_default=db.text("(now() at time zone 'utc')"),
    )
    updated_at = db.Column(
        "updated_at",
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        server_default=db.text("(now() at time zone 'utc')"),
        onupdate=datetime.utcnow,
    )
