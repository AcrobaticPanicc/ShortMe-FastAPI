from typing import List, Optional
from schemas.url import UrlResponse
from pydantic import BaseModel, EmailStr


class _UserBase(BaseModel):
    email: EmailStr = None
    full_name: Optional[str] = None


class UserCreate(_UserBase):
    password: str


class UserResponse(_UserBase):
    id_: int
    is_active: bool
    short_urls: List[UrlResponse] = []
    email: str

    class Config:
        orm_mode = True
