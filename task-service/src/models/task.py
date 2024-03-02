import uuid
from datetime import datetime

from sqlalchemy import Enum, DateTime
from sqlalchemy.dialects.postgresql import UUID

from src.database import db
from src.enums.status import TaskStatus
from src.models.base import Base


class Task(Base):
    __tablename__ = "task"

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(UUID(as_uuid=True), nullable=False, default=uuid.uuid4)
    title = db.Column(db.String(128), nullable=False, default="", server_default=db.text("''"))
    short_title = db.Column(db.String(50), nullable=False, default="", server_default=db.text("''"))
    description = db.Column(db.Text, nullable=False, default="", server_default=db.text("''"))
    jira_id = db.Column(db.Integer)
    status = db.Column(
        Enum(TaskStatus),
        nullable=False,
        default=TaskStatus.OPEN,
        server_default=db.text(f"'{TaskStatus.OPEN.value}'"),
    )
    assignee_id = db.Column(db.Integer, db.ForeignKey("users.id"))
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
    assignee = db.relationship("User", foreign_keys=[assignee_id])

    @property
    def long_title(self) -> str:
        return (
            f"[{self.jira_id}]-{self.short_title})"
            if self.jira_id
            else self.title
        )
