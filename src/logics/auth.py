from fastapi import HTTPException, status
from passlib.handlers.pbkdf2 import pbkdf2_sha256

from src.models.auth_model import RegisterInputModel, RegisterOutputModel, LoginInputModel, LoginOutputModel
from src.models.user_model import UserModel

from src.repositories.repository import Repository
from src.utils import token
from src.utils.decorators.atomic import atomic
from src.utils.settings import settings


class AuthLogic:
    def __init__(self) -> None:
        self.repository = Repository()

    def login(self, input_model: LoginInputModel) -> LoginOutputModel:
        user_model = UserModel(email=input_model.email)
        user_data = self.repository.get_user(user_model)
        if not user_data:
            # fix this error
            raise ValueError("your email or password is not correct")
        if not pbkdf2_sha256.verify(input_model.password.get_secret_value(), user_data.password):
            # fix this error
            raise ValueError("your email or password is not correct")
        # send user id to jwt...
        access_token = token.generate_jwt_token(
            identity=input_model.email,
            token_type="access",
            lifetime=settings.ACCESS_TOKEN_EXPIRE,
            claims=None,
            headers=None
        )
        refresh_token = token.generate_jwt_token(
            identity=input_model.email,
            token_type="refresh",
            lifetime=settings.REFRESH_TOKEN_EXPIRE,
            claims=None,
            headers=None
        )

        # Store refresh token and other metadata in redis
        # await add_refresh_token_to_redis(redis_client, user, refresh_token, forwarded_for, user_agent, request.fingerprint)

        return LoginOutputModel(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    # TODO: this must be atomic
    @atomic
    def register(self, input_model: RegisterInputModel) -> RegisterOutputModel:
        # forwarded_for, user_agent = get_auth_headers()

        user_model = UserModel(email=input_model.email, password=input_model.password)
        user = self.repository.get_user(user_model)
        if user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='User already exists')
        self.repository.create_user(user_model)

        # Create tokens
        # TODO: fix this in function...
        # identity should by email???

        # send user id to jwt...
        access_token = token.generate_jwt_token(
            identity=input_model.email,
            token_type="access",
            lifetime=settings.ACCESS_TOKEN_EXPIRE,
            claims=None,
            headers=None
        )
        refresh_token = token.generate_jwt_token(
            identity=input_model.email,
            token_type="refresh",
            lifetime=settings.REFRESH_TOKEN_EXPIRE,
            claims=None,
            headers=None
        )

        # Store refresh token and other metadata in redis
        # await add_refresh_token_to_redis(redis_client, user, refresh_token, forwarded_for, user_agent, request.fingerprint)

        return RegisterOutputModel(
            access_token=access_token,
            refresh_token=refresh_token,
        )
