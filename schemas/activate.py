import pydantic as pydantic


class _Otp(pydantic.BaseModel):
    pass


class Otp(_Otp):
    otp: str
