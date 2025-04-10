from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str

    model_config = {
        "from_attributes": True
    }

class UserLogin(BaseModel):
    email: EmailStr
    password: str

    model_config = {
        "from_attributes": True
    }

class Token(BaseModel):
    access_token: str
    token_type: str

    model_config = {
        "from_attributes": True
    }

class TokenData(BaseModel):
    email: str | None = None

    model_config = {
        "from_attributes": True
    } 