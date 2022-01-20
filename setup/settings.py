from pydantic import BaseSettings


class Settings(BaseSettings):
    secret: str
    database_uri: str = None
    token_url: str = "/user/token"

    class Config:
        env_file = ".env"


settings = Settings()
