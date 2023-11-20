from sqlalchemy import select, and_

from src.models.entities import UserEntity, SourceEntity, FeedEntity, BookmarkEntity
from src.models.feed_model import (
    GetUserSourcesModel,
    SourceModel,
    FeedModel,
    BookmarkModel,
    GetUserFeedsModel
)
from src.models.user_model import UserModel
from src.utils.orm.sqlalchemy_adapter import SqlAlchemyAdapter


class PostgresAdapter(SqlAlchemyAdapter):
    def __init__(self) -> None:
        super().__init__()

    def create_user(self, input_model: UserModel) -> UserModel:
        user = UserEntity(**input_model.model_dump(exclude_unset=True, exclude_none=True))
        user_entity = self.create(user, return_data=True)
        return UserModel.model_validate(user_entity)

    def get_user_by_email(self, input_model: UserModel) -> UserModel | None:
        query = select(UserEntity).where(UserEntity.email == input_model.email)
        if (user_entity := self.execute(query).scalar()) is None:
            return None
        return UserModel.model_validate(user_entity)

    def get_user_by_id(self, input_model: UserModel | BookmarkModel) -> UserModel | None:
        query = select(UserEntity).where(UserEntity.user_id == input_model.user_id)
        if (user_entity := self.execute(query).scalar()) is None:
            return None
        return UserModel.model_validate(user_entity)

    def get_user_sources(self, input_model: UserModel) -> GetUserSourcesModel | None:
        query = select(SourceEntity).where(SourceEntity.user_id == input_model.user_id)
        if (source_entities := self.scalars(query).all()) is None:
            return None
        response_model = [SourceModel.model_validate(q) for q in source_entities]
        return GetUserSourcesModel(user_sources=response_model)

    def create_source(self, input_model: SourceModel) -> SourceModel:
        query = select(SourceEntity).where(
            and_(
                SourceEntity.user_id==input_model.user_id,
                SourceEntity.link == input_model.link
            )
        )
        if (query_response := self.execute(query).scalar()) is None:
            source = SourceEntity(**input_model.model_dump(exclude_unset=True, exclude_none=True))
            source_entity = self.create(source, return_data=True)
            return SourceModel.model_validate(source_entity)
        return SourceModel.model_validate(query_response)

    def create_feed(self, input_model: FeedModel) -> FeedModel:
        feed = FeedEntity(**input_model.model_dump(exclude_unset=True, exclude_none=True))
        feed_entity = self.create(feed, return_data=True)
        return FeedModel.model_validate(feed_entity)

    def get_feed_by_id(self, input_model: UserModel) -> FeedModel | None:
        query = select(FeedEntity).where(
            and_(
                FeedEntity.feed_id == input_model.feed_id,
                FeedEntity.user_id == input_model.user_id
            )
        )
        if (feed_entity := self.execute(query).scalar()) is None:
            return None
        return FeedModel.model_validate(feed_entity)

    def is_exist_feed(self, input_model: FeedModel) -> FeedModel | None:
        query = select(FeedEntity).where(
            and_(
                FeedEntity.title == input_model.title,
                FeedEntity.link == input_model.link,
                FeedEntity.summary == input_model.summary,
                FeedEntity.published == input_model.published
            )
        )
        if (feed_entity := self.execute(query).scalar()) is None:
            return None
        return FeedModel.model_validate(feed_entity)

    def create_bookmark(self, input_model) -> BookmarkModel:
        bookmark = BookmarkEntity(**input_model.model_dump(exclude_unset=True, exclude_none=True))
        bookmark_entity = self.create(bookmark, return_data=True)
        return BookmarkModel.model_validate(bookmark_entity)

    def get_bookmark(self, input_model: BookmarkModel) -> BookmarkModel | None:
        query = select(BookmarkEntity).where(BookmarkEntity.bookmark_id == input_model.bookmark_id)
        if (bookmark_entity := self.execute(query).scalar()) is None:
            return None
        return BookmarkModel.model_validate(bookmark_entity)

    def get_user_bookmarks(self, input_model: UserModel) -> GetUserFeedsModel:
        query = select(FeedEntity).join(BookmarkEntity).where(
            and_(FeedEntity.user_id == input_model.user_id, BookmarkEntity.user_id == input_model.user_id))
        bookmark_entities = self.scalars(query).all()
        response_model = [FeedModel.model_validate(e) for e in bookmark_entities]
        return GetUserFeedsModel(user_feeds=response_model)
