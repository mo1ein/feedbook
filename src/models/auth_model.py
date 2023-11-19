from uuid import UUID

from passlib.handlers.pbkdf2 import pbkdf2_sha256
from pydantic import BaseModel, StrictStr, EmailStr, SecretStr, field_validator, ConfigDict
import re

from src.models.base_model import BaseFeedBookModel


class LoginInputModel(BaseFeedBookModel):
    email: EmailStr  # TODO: can be username
    password: SecretStr


class LoginOutputModel(BaseFeedBookModel):
    access_token: StrictStr
    refresh_token: StrictStr


class RegisterInputModel(BaseFeedBookModel):
    email: EmailStr
    password: SecretStr

    @field_validator("password")
    def _validate_password(cls, password):
        password = password.get_secret_value()
        special_chars_pattern = (
            r"[\\!\\\"\\#\\$\\%\\&\\'\\(\\)\\*\\+\\,\\-\\.\\/\\:\\;\\<\\>\\=\\?\\@\\{\\}\\\\\\^\\_\\`\\~]"
        )
        number_chars_pattern = r"[0-9]"
        lowercase_chars_pattern = r"[a-z]"
        uppercase_chars_pattern = r"[A-Z]"
        if password is None:
            raise ValueError("Make sure your password is at least 6 letters")
        if len(password) < 8:
            raise ValueError("Make sure your password is at least 6 letters")
        if re.search(lowercase_chars_pattern, password) is None:
            raise ValueError("Make sure your password has a lower letter")
        if re.search(uppercase_chars_pattern, password) is None:
            raise ValueError("Make sure your password has a capital letter")
        if re.search(number_chars_pattern, password) is None:
            raise ValueError("Make sure your password has a number")
        if re.search(special_chars_pattern, password) is None:
            raise ValueError("Make sure your password has a special letter")
        return pbkdf2_sha256.hash(password)


class RegisterOutputModel(BaseFeedBookModel):
    access_token: StrictStr
    refresh_token: StrictStr


class VerifyAccessTokenInputModel(BaseFeedBookModel):
    access_token: StrictStr


class VerifyAccessTokenOutputModel(BaseFeedBookModel):
    user_id: UUID
