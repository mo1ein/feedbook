import logging

from src.utils.base_utils import BaseUtils
import os
from typing import Any, Type


class BaseOrmConfig:
    # fix
    ORM_DATABASE: str = "postgres"
    ORM_ECHO: bool = False
    ORM_ECHO_POOL: bool = False
    ORM_ENABLE_FROM_LINTING: bool = True
    ORM_HIDE_PARAMETERS: bool = False
    #fix
    # ORM_HOST: str = "feedbook_db"
    ORM_HOST: str = "localhost"
    ORM_ISOLATION_LEVEL: str = "SERIALIZABLE"
    #fix
    ORM_PASSWORD: str = "postgres"
    ORM_POLL_MAX_OVERFLOW: int = 1
    ORM_POOL_PRE_PING: bool = True
    ORM_POOL_RECYCLE_SECONDS: int = 10 * 60
    ORM_POOL_RESET_ON_RETURN: str = "rollback"
    ORM_POOL_SIZE: int = 20
    ORM_POOL_TIMEOUT: int = 30
    ORM_POOL_USE_LIFO: bool = True
    ORM_PORT: int = 5432
    ORM_QUERY_CACHE_SIZE: int = 500
    #fix
    ORM_USERNAME: str = "postgres"


class BaseFastAPIConfig:
    FASTAPI_ACCESS_LOG: bool = True
    FASTAPI_BACKLOG: int = 2048
    FASTAPI_DATE_HEADER: bool = True
    FASTAPI_FORWARDED_ALLOW_IPS: list = None
    FASTAPI_LIMIT_CONCURRENCY: int = None
    FASTAPI_LIMIT_MAX_REQUESTS: int = None
    FASTAPI_PROXY_HEADERS: bool = True
    FASTAPI_RELOAD: bool = False
    FASTAPI_SERVER_HEADER: bool = True
    FASTAPI_SERVE_HOST: str = "0.0.0.0"
    FASTAPI_SERVE_PORT: int = 8500
    FASTAPI_TIMEOUT_GRACEFUL_SHUTDOWN: int = None
    FASTAPI_TIMEOUT_KEEP_ALIVE: int = 5
    FASTAPI_WS_MAX_SIZE: int = 16777216
    FASTAPI_WS_PER_MESSAGE_DEFLATE: bool = True
    FASTAPI_WS_PING_INTERVAL: float = 20.0
    FASTAPI_WS_PING_TIMEOUT: float = 20.0


class BaseConfig(BaseOrmConfig, BaseFastAPIConfig):
    LOGGING_LEVEL: int = logging.INFO


class Configuration:
    _config_class = BaseConfig

    @classmethod
    def _get_all_annotated_fields(cls, class_: Type) -> dict:
        all_base_classes = BaseUtils.all_base_classes(class_)
        all_inherited_fields = {}
        for base in all_base_classes:
            if hasattr(base, "__annotations__"):
                for key, value in base.__annotations__.items():
                    all_inherited_fields[key] = value

        return all_inherited_fields

    @classmethod
    def _find_dotenv(cls, filename: str, alternative_env_search_dir: str | None) -> str:
        from dotenv import find_dotenv

        file_path = ""
        try:
            file_path = find_dotenv(filename=filename)
        except Exception:
            print("Warning: First try to find .env file failed!")
        if len(file_path) == 0 and alternative_env_search_dir is not None:
            for dirname in BaseUtils.walk_all_parent_dirs(alternative_env_search_dir):
                check_path = os.path.join(dirname, filename)
                if os.path.isfile(check_path):
                    return check_path

        return file_path

    @classmethod
    def apply(
            cls,
            cls_type: Type | None = None,
            is_test: bool = False,
            alternative_env_search_dir: str | None = None,
            silent: bool = False,
    ) -> None:
        cls._inject_config(alternative_env_search_dir, cls_type, is_test, silent)

    @classmethod
    def _inject_config(cls, alternative_env_search_dir, cls_type: Type | None, is_test, silent):
        from dotenv import dotenv_values, load_dotenv

        if cls_type:
            cls._config_class = cls_type
        if alternative_env_search_dir is None and not silent:
            print(
                "Warning: alternative_env_search_dir is set to None. .env files can not be found when venv dir located"
                "\noutside of project main directory. you can use alternative_env_search_dir=__file__ to avoid it."
                "\n use silent = True to suppress this warning"
            )
        filename = ".env.test" if is_test else ".env"
        dotenv_values = dotenv_values(
            cls._find_dotenv(filename=filename, alternative_env_search_dir=alternative_env_search_dir)
        )
        all_annotated_fields = cls._get_all_annotated_fields(cls._config_class)
        for env_attr in dotenv_values:
            if not hasattr(cls._config_class, env_attr):
                # set .env field to class to replace with env values in next loop
                setattr(cls._config_class, env_attr, None)
        load_dotenv(cls._find_dotenv(filename=filename, alternative_env_search_dir=alternative_env_search_dir))
        for attr_name in dir(cls._config_class):
            if attr_name.startswith("__") or callable(getattr(cls._config_class, attr_name)):
                continue

            from_env = os.getenv(attr_name)
            if not from_env:
                continue

            annotated_type = all_annotated_fields.get(attr_name)

            try:
                final_value = cls._set_value_for_class(cls._config_class, attr_name, from_env, annotated_type)
                setattr(cls._config_class, attr_name, final_value)

            except Exception as e:
                raise Exception(
                    f"Configuration field format Exception: "
                    f"For field {attr_name} got {from_env}  expected {annotated_type!s}."
                ) from e

    @classmethod
    def config(cls) -> Type[BaseConfig]:
        return cls._config_class

    @classmethod
    def _set_value_for_class(
            cls, class_: Type, attr_name: str, env_value: str, annotated_field_class: Type | None = None
    ) -> Any:
        class_value = getattr(class_, attr_name)
        if annotated_field_class:
            if type(annotated_field_class).__name__ != "_GenericAlias" and issubclass(annotated_field_class, str):
                return env_value
            return eval(env_value)
        if class_value:
            return env_value if isinstance(class_value, str) else eval(env_value)
        return env_value
