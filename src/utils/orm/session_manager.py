from abc import abstractmethod

from sqlalchemy import URL, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from src.utils.configs import Configuration
from src.utils.metaclasses.singelton import Singleton


class SessionPort:
    @abstractmethod
    def get_session(self):
        raise NotImplementedError

    @abstractmethod
    def remove_session(self):
        raise NotImplementedError


class SessionManager(SessionPort, metaclass=Singleton):
    def __init__(self) -> None:
        self._session_generator = self._get_session_generator()

    def get_session(self):
        return self._session_generator()

    def remove_session(self):
        self._session_generator.remove()

    def _get_session_generator(self):
        engine = self._create_engine()
        session_maker = sessionmaker(engine)
        session_generator = scoped_session(session_maker)
        return session_generator

    @staticmethod
    def _create_engine():
        url = URL.create(
            drivername="postgresql+psycopg",
            username=Configuration.config().ORM_USERNAME,
            password=Configuration.config().ORM_PASSWORD,
            host=Configuration.config().ORM_HOST,
            port=Configuration.config().ORM_PORT,
            database=Configuration.config().ORM_DATABASE,
        )
        return create_engine(
            url,
            isolation_level=Configuration.config().ORM_ISOLATION_LEVEL,
            echo=Configuration.config().ORM_ECHO,
            echo_pool=Configuration.config().ORM_ECHO_POOL,
            enable_from_linting=Configuration.config().ORM_ENABLE_FROM_LINTING,
            hide_parameters=Configuration.config().ORM_HIDE_PARAMETERS,
            pool_pre_ping=Configuration.config().ORM_POOL_PRE_PING,
            pool_size=Configuration.config().ORM_POOL_SIZE,
            pool_recycle=Configuration.config().ORM_POOL_RECYCLE_SECONDS,
            pool_reset_on_return=Configuration.config().ORM_POOL_RESET_ON_RETURN,
            pool_timeout=Configuration.config().ORM_POOL_TIMEOUT,
            pool_use_lifo=Configuration.config().ORM_POOL_USE_LIFO,
            query_cache_size=Configuration.config().ORM_QUERY_CACHE_SIZE,
            max_overflow=Configuration.config().ORM_POLL_MAX_OVERFLOW,
        )