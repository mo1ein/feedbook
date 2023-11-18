# TODO add last_name first_name?? username??
import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, UUID, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, DeclarativeBase, relationship


# fix all type hints

class BaseEntity(DeclarativeBase):
    created_at: Mapped[datetime] = Column(DateTime(), server_default="DEFAULT", nullable=False)


class FeedEntity(BaseEntity):
    __tablename__ = "feed"
    feed_id: Mapped[uuid.UUID] = Column(UUID(as_uuid=True), primary_key=True, server_default="DEFAULT")
    user_id = Column(UUID, ForeignKey("users.user_id"), nullable=False)
    title = Column(String(), nullable=False)
    link = Column(String(), nullable=False)
    summary = Column(String(), nullable=False)
    author = Column(String(), nullable=False)
    published = Column(String(), nullable=False)

    user = relationship("UserEntity", foreign_keys=[user_id])



class SourceEntity(BaseEntity):
    __tablename__ = "source"
    source_id: Mapped[uuid.UUID] = Column(UUID(as_uuid=True), primary_key=True, server_default="DEFAULT")
    user_id = Column(UUID, ForeignKey("users.user_id"), nullable=False)
    link = Column(String(), nullable=False)

    user = relationship("UserEntity", foreign_keys=[user_id])


class BookmarkEntity(BaseEntity):
    __tablename__ = "bookmark"
    bookmark_id: Mapped[uuid.UUID] = Column(UUID(as_uuid=True), primary_key=True, server_default="DEFAULT")
    feed_id = Column(UUID, ForeignKey("feed.feed_id"), nullable=False)
    user_id = Column(UUID, ForeignKey("users.user_id"), nullable=False)
    created_at: Mapped[datetime] = Column(DateTime(), server_default="DEFAULT", nullable=False)
    updated_at: Mapped[datetime] = Column(DateTime(), nullable=False)

    user = relationship("UserEntity", foreign_keys=[user_id])
    feed = relationship("FeedEntity", foreign_keys=[feed_id])




class UserEntity(BaseEntity):
    __tablename__ = "users"
    user_id: Mapped[uuid.UUID] = Column(UUID(as_uuid=True), primary_key=True, server_default="DEFAULT")
    email = Column(String(), unique=True, nullable=False)
    password = Column(String(), nullable=False)
    is_active = Column(Boolean(), nullable=False)
