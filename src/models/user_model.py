from uuid import UUID

from pydantic import EmailStr, PastDatetime, ConfigDict, StrictStr

from src.models.base_model import BaseFeedBookModel


class UserModel(BaseFeedBookModel):
    user_id: UUID | None = None
    email: EmailStr | None = None
    password: StrictStr | None = None
    is_active: bool | None = None
    created_at: PastDatetime | None = None
