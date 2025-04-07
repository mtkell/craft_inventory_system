from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str | None
    full_name: str | None
    password: str

class UserRead(BaseModel):
    id: int
    username: str
    email: str | None
    full_name: str | None

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str
