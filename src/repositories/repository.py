from src.models.feed_model import GetUserSourcesModel, SourceModel, FeedModel, BookmarkModel, GetUserBookmarksModel, \
    GetUserFeedsModel
from src.models.user_model import UserModel
from src.repositories.adapters.postgres_adapter import PostgresAdapter


class Repository:
    def __init__(self) -> None:
        self.postgres_adapter = PostgresAdapter()

    def create_user(self, input_model: UserModel) -> UserModel:
        return self.postgres_adapter.create_user(input_model)

    def get_user_by_email(self, input_model: UserModel) -> UserModel | None:
        return self.postgres_adapter.get_user_by_email(input_model)

    def get_user_by_id(self, input_model: UserModel | BookmarkModel) -> UserModel | None:
        return self.postgres_adapter.get_user_by_id(input_model)

    def get_user_sources(self, input_model: UserModel) -> GetUserSourcesModel:
        return self.postgres_adapter.get_user_sources(input_model)

    def add_user_source(self, input_model: SourceModel) -> SourceModel:
        return self.postgres_adapter.create_source(input_model)

    def get_user_bookmarks(self, input_model: UserModel) -> GetUserFeedsModel:
        return self.postgres_adapter.get_user_bookmarks(input_model)

    def create_bookmark(self, input_model: BookmarkModel):
        return self.postgres_adapter.create_bookmark(input_model)

    def get_user_feeds(self, input_model: UserModel):
        ...

    def get_feed(self, input_model) -> FeedModel:
        return self.postgres_adapter.get_feed(input_model)

    def get_bookmark(self, input_model) -> BookmarkModel:
        return self.postgres_adapter.get_bookmark(input_model)

    def create_feed(self, input_model: FeedModel) -> FeedModel:
        return self.postgres_adapter.create_feed(input_model)
