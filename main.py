import uvicorn

from src import logics
from src.logics.auth import AuthLogic
from src.models.auth_model import RegisterOutputModel, LoginOutputModel, RegisterInputModel, LoginInputModel
from src.utils import token
from fastapi import FastAPI, status

from src.utils.settings import settings

app = FastAPI()


# TODO: better route
@app.post(
    "/auth/register",
    response_model=RegisterOutputModel,
    # fix this
    tags=["AUTH_API"],
    status_code=status.HTTP_201_CREATED
)
# TODO: this should be async or not?
def register(input_model: RegisterInputModel) -> RegisterOutputModel:
    """Register user and create JWT access and refresh tokens"""
    return AuthLogic().register(input_model)


# TODO: better route
@app.post(
    "/auth/login",
    response_model=LoginOutputModel,
    # fix this
    tags=["AUTH_API"],
    # its true??
    status_code=status.HTTP_200_OK
)
def login(input_model: LoginInputModel) -> LoginOutputModel:
    return AuthLogic().login(input_model)


# TODO: refresh_token


uvicorn.run(app)
