from uuid import UUID

from pydantic import BaseModel, PastDatetime, ConfigDict, StrictStr


class SourceModel(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_default=True, from_attributes=True, validate_assignment=True)

    source_id: UUID | None = None
    user_id: UUID | None = None
    link: StrictStr | None = None
    created_at: PastDatetime | None = None


class GetUserSourcesModel(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_default=True, from_attributes=True, validate_assignment=True)
    user_sources: list[SourceModel]


class FeedModel(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_default=True, from_attributes=True, validate_assignment=True)
    feed_id: UUID | None = None
    user_id: UUID | None = None
    title: StrictStr | None = None
    link: StrictStr | None = None
    summary: StrictStr | None = None
    author: StrictStr | None = None
    published: StrictStr | None = None
    created_at: PastDatetime | None = None


class GetUserFeedsModel(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_default=True, from_attributes=True, validate_assignment=True)
    user_feeds: list[FeedModel]


class BookmarkModel(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_default=True, from_attributes=True, validate_assignment=True)

    bookmark_id: UUID | None = None
    feed_id: UUID | None = None
    user_id: UUID | None = None
    created_at: PastDatetime | None = None
    updated_at: PastDatetime | None = None

class GetUserBookmarksModel(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_default=True, from_attributes=True, validate_assignment=True)

    user_bookmarks: list[BookmarkModel]


