import datetime as _dt
from typing import Optional
import pydantic as pydantic
from type_validators.validators import Date, Url, CustomUrl


class _ShortUrlBase(pydantic.BaseModel):
    pass


class ShortenUrl(_ShortUrlBase):
    long_url: Url
    is_active: bool = True
    password: str = None
    available_clicks: Optional[int] = -1
    expires_at: Optional[Date] = None
    custom_url: Optional[CustomUrl] = None


class ShortUrl(_ShortUrlBase):
    id_: int
    owner_id: int
    date_created: _dt.datetime
    custom_url: Optional[CustomUrl] = None


class UrlResponse(ShortenUrl):
    expires_at: str
    short_url: str
    date_created: str
