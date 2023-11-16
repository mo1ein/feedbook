from uuid import UUID

from pydantic import BaseModel, EmailStr, PastDatetime, ConfigDict, StrictStr


class UserModel(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_default=True, from_attributes=True, validate_assignment=True)

    id: UUID | None = None
    email: EmailStr | None = None
    password: StrictStr | None = None
    created_at: PastDatetime | None = None
