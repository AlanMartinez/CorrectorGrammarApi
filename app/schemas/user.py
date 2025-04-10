from pydantic import BaseModel, EmailStr
from .dictionary import DictionaryItemResponse

class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    dictionary_items: list[DictionaryItemResponse] = []

    model_config = {
        "from_attributes": True
    } 