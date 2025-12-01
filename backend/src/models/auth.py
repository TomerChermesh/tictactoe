from pydantic import BaseModel, EmailStr
from src.models.users import UserDocument

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    ok: bool
    user: UserDocument
    accessToken: str
    tokenType: str = 'bearer'