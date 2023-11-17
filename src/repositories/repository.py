from src.models.feed_model import GetUserSourcesModel, SourceModel
from src.models.user_model import UserModel
from src.repositories.adapters.postgres_adapter import PostgresAdapter


class Repository:
    def __init__(self) -> None:
        self.postgres_adapter = PostgresAdapter()

    def create_user(self, input_model: UserModel) -> UserModel:
        return self.postgres_adapter.create_user(input_model)

    def get_user(self, input_model: UserModel) -> UserModel:
        return self.postgres_adapter.get_user(input_model)

    def get_user_sources(self, input_model: UserModel) -> GetUserSourcesModel:
        return self.postgres_adapter.get_user_sources(input_model)

    def add_user_source(self, input_model: SourceModel):
        self.postgres_adapter.create_source(input_model)