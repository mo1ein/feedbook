from typing import Type
from uuid import UUID

from sqlalchemy import Executable

from src.models.entities import UserEntity, BaseEntity
from src.utils.exceptions import InvalidEntityTypeException
from src.utils.orm.session_manager import SessionManager
from src.utils.orm.sqlalchemy_port import SqlAlchemyPort, AnyExecuteParams


class BaseSqlAlchemyAdapter(SqlAlchemyPort):
    def get_session(self):
        raise NotImplementedError

    def create(self, entity, return_data: bool = False):
        if not isinstance(entity, BaseEntity):
            raise InvalidEntityTypeException(entity, BaseEntity)
        session = self.get_session()
        session.add(entity)
        if return_data:
            session.flush()
            return entity

    def bulk_create(self, entities, return_data: bool = False):
        session = self.get_session()
        session.add_all(entities)
        if return_data:
            session.flush()
            return entities

    def get_by_uuid(self, entity_type: Type, entity_uuid: UUID):
        if not issubclass(entity_type, BaseEntity):
            raise InvalidEntityTypeException(entity_type, BaseEntity)
        if not isinstance(entity_uuid, UUID):
            raise InvalidEntityTypeException(entity_uuid, UUID)
        session = self.get_session()
        return session.get(entity_type, entity_uuid)

    def delete(self, entity: BaseEntity) -> None:
        if not isinstance(entity, UserEntity):
            raise InvalidEntityTypeException(entity, BaseEntity)
        session = self.get_session()
        session.delete(entity)

    def bulk_delete(self, entities: list[BaseEntity]) -> None:
        for entity in entities:
            self.delete(entity)

    def execute(self, statement: Executable, params: AnyExecuteParams | None = None):
        session = self.get_session()
        return session.execute(statement, params)

    def scalars(self, statement: Executable, params: AnyExecuteParams | None = None):
        session = self.get_session()
        return session.scalars(statement, params)


class SqlAlchemyAdapter(BaseSqlAlchemyAdapter):
    def __init__(self):
        self.session_manager = SessionManager()

    def get_session(self):
        return self.session_manager.get_session()
