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


class GetUserFeedsModel(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_default=True, from_attributes=True, validate_assignment=True)

    class FeedModel(BaseModel):
        model_config = ConfigDict(extra="forbid", validate_default=True, from_attributes=True, validate_assignment=True)
        feed_id: UUID
        title: StrictStr
        link: StrictStr
        summary: StrictStr
        author: StrictStr
        published: StrictStr
        created_at: PastDatetime

    user_feeds: list[FeedModel]
