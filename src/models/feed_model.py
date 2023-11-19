from uuid import UUID

from pydantic import PastDatetime, StrictStr

from src.models.base_model import BaseFeedBookModel


class SourceModel(BaseFeedBookModel):
    source_id: UUID | None = None
    user_id: UUID | None = None
    link: StrictStr | None = None
    created_at: PastDatetime | None = None


class GetUserSourcesModel(BaseFeedBookModel):
    user_sources: list[SourceModel]


class FeedModel(BaseFeedBookModel):
    feed_id: UUID | None = None
    user_id: UUID | None = None
    title: StrictStr | None = None
    link: StrictStr | None = None
    summary: StrictStr | None = None
    author: StrictStr | None = None
    published: StrictStr | None = None
    created_at: PastDatetime | None = None


class GetUserFeedsModel(BaseFeedBookModel):
    user_feeds: list[FeedModel]


class BookmarkModel(BaseFeedBookModel):
    bookmark_id: UUID | None = None
    feed_id: UUID | None = None
    user_id: UUID | None = None
    created_at: PastDatetime | None = None
    updated_at: PastDatetime | None = None


class GetUserBookmarksModel(BaseFeedBookModel):
    user_bookmarks: list[BookmarkModel]
