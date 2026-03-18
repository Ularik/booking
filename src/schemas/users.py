from pydantic import BaseModel, Field, ConfigDict


class UsersRequestSchema(BaseModel):
    username: str
    nik_name: str = Field(None)
    password: str


class UserLoginSchema(BaseModel):
    username: str
    password: str


class UserAddSchema(BaseModel):
    username: str
    nik_name: str | None = Field(None)
    hashed_password: str


class UserOutSchema(BaseModel):
    id: int
    username: str
    nik_name: str | None

    model_config = ConfigDict(from_attributes=True)


class UserHashedPswdSchema(UserAddSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)
