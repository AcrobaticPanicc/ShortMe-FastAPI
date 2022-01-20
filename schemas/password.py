import pydantic as pydantic


class Password(pydantic.BaseModel):
    password: str = None
