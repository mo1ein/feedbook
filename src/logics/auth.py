from fastapi import HTTPException, status
from passlib.handlers.pbkdf2 import pbkdf2_sha256

from src.models.auth_model import (
    RegisterInputModel,
    RegisterOutputModel,
    LoginInputModel,
    LoginOutputModel,
    VerifyAccessTokenInputModel,
    VerifyAccessTokenOutputModel
)
from src.models.user_model import UserModel

from src.repositories.repository import Repository
from src.utils import token
from src.utils.configs import AuthConfigs
from src.utils.decorators.atomic import atomic
from src.utils.token import decode_jwt_token


class AuthLogic:
    def __init__(self) -> None:
        self.repository = Repository()

    @atomic
    def login(self, input_model: LoginInputModel) -> LoginOutputModel:
        user_model = UserModel(email=input_model.email)
        user_data = self.repository.get_user_by_email(user_model)

        if not user_data:
            raise HTTPException(status_code=401, detail="your email or password is not correct")
        if not pbkdf2_sha256.verify(input_model.password.get_secret_value(), user_data.password):
            raise HTTPException(status_code=401, detail="your email or password is not correct")

        access_token = token.generate_jwt_token(
            identity=str(user_data.user_id),
            token_type="access",
            lifetime=AuthConfigs.ACCESS_TOKEN_EXPIRE,
            claims=None,
            headers=None
        )
        refresh_token = token.generate_jwt_token(
            identity=str(user_data.user_id),
            token_type="refresh",
            lifetime=AuthConfigs.REFRESH_TOKEN_EXPIRE,
            claims=None,
            headers=None
        )
        return LoginOutputModel(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    @atomic
    def register(self, input_model: RegisterInputModel) -> RegisterOutputModel:
        user_model = UserModel(
            name=input_model.name,
            last_name=input_model.last_name,
            email=input_model.email,
            password=input_model.password,
            is_active=True
        )
        user = self.repository.get_user_by_email(user_model)
        if user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='User already exists')
        created_user = self.repository.create_user(user_model)

        access_token = token.generate_jwt_token(
            identity=str(created_user.user_id),
            token_type="access",
            lifetime=AuthConfigs.ACCESS_TOKEN_EXPIRE,
            claims=None,
            headers=None
        )
        refresh_token = token.generate_jwt_token(
            identity=str(created_user.user_id),
            token_type="refresh",
            lifetime=AuthConfigs.REFRESH_TOKEN_EXPIRE,
            claims=None,
            headers=None
        )
        return RegisterOutputModel(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    def verify_access_token(self, input_model: VerifyAccessTokenInputModel) -> VerifyAccessTokenOutputModel:
        decoded_token = decode_jwt_token(input_model.access_token)
        return VerifyAccessTokenOutputModel(user_id=decoded_token.get("user_id"))
