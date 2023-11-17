from uuid import UUID

from passlib.handlers.pbkdf2 import pbkdf2_sha256
from pydantic import BaseModel, StrictStr, EmailStr, SecretStr, field_validator, ConfigDict
import re


# move config to a base class

class LoginInputModel(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_default=True, from_attributes=True, validate_assignment=True)

    email: EmailStr  # TODO: can be username
    password: SecretStr


class LoginOutputModel(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_default=True, from_attributes=True, validate_assignment=True)
    access_token: StrictStr
    refresh_token: StrictStr


class RegisterInputModel(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_default=True, from_attributes=True, validate_assignment=True)

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


class RegisterOutputModel(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_default=True, from_attributes=True, validate_assignment=True)

    access_token: StrictStr
    refresh_token: StrictStr


class Token(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_default=True, from_attributes=True, validate_assignment=True)

    access_token: StrictStr
    refresh_token: StrictStr
    token_type: StrictStr


class VerifyAccessTokenInputModel(BaseModel):
    access_token: StrictStr


class VerifyAccessTokenOutputModel(BaseModel):
    user_id: UUID
