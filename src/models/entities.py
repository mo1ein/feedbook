# TODO add last_name first_name?? username??
import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, UUID
from sqlalchemy.orm import Mapped, DeclarativeBase


# fix all type hints

class BaseEntity(DeclarativeBase):
    ...


class UserEntity(BaseEntity):
    __tablename__ = "users"
    id: Mapped[uuid.UUID] = Column(UUID(as_uuid=True), primary_key=True, server_default="DEFAULT")
    email = Column(String, unique=True, nullable=False)
    password = Column(String(), nullable=False)
    created_at: Mapped[datetime] = Column(DateTime(), server_default="DEFAULT", nullable=False)
