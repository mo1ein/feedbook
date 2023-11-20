from src.logics.auth import AuthLogic
from src.models.auth_model import RegisterOutputModel, LoginOutputModel, RegisterInputModel, LoginInputModel
from fastapi import status, APIRouter

from src.models.service_enum import ServiceType

public_routes = APIRouter()


@public_routes.post(
    "/auth/register",
    response_model=RegisterOutputModel,
    tags=[ServiceType.AUTH_API],
    status_code=status.HTTP_201_CREATED
)
def register(input_model: RegisterInputModel) -> RegisterOutputModel:
    """Register user and create JWT access and refresh tokens"""
    return AuthLogic().register(input_model)


@public_routes.post(
    "/auth/login",
    response_model=LoginOutputModel,
    tags=[ServiceType.AUTH_API],
    status_code=status.HTTP_200_OK
)
def login(input_model: LoginInputModel) -> LoginOutputModel:
    return AuthLogic().login(input_model)
