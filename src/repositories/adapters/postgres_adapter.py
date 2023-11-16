from sqlalchemy import select

from src.models.entities import UserEntity
from src.models.user_model import UserModel
from src.utils.orm.sqlalchemy_adapter import SqlAlchemyAdapter


class PostgresAdapter(SqlAlchemyAdapter):
    def __init__(self) -> None:
        super().__init__()

    def create_user(self, input_model: UserModel) -> UserModel:
        user = UserEntity(**input_model.model_dump(exclude_unset=True, exclude_none=True))
        user_entity = self.create(user, return_data=True)
        return UserModel.model_validate(user_entity)

    def get_user(self, input_model: UserModel) -> UserModel | None:
        query = select(UserEntity).where(UserEntity.email == input_model.email)
        if (user_entity := self.execute(query).scalar()) is None:
            return None
        return UserModel.model_validate(user_entity)
