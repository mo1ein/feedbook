from uuid import UUID

from pydantic import EmailStr, PastDatetime, StrictStr

from src.models.base_model import BaseFeedBookModel


class UserModel(BaseFeedBookModel):
    user_id: UUID | None = None
    name: StrictStr | None = None
    last_name: StrictStr | None = None
    email: EmailStr | None = None
    password: StrictStr | None = None
    is_active: bool = True
    created_at: PastDatetime | None = None
