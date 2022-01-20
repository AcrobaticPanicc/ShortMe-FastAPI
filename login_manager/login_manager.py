from fastapi_login import LoginManager
from setup.settings import settings

manager = LoginManager(settings.secret, settings.token_url)


def hash_password(plaintext_password: str):
    """ Return the hash of a password """
    return manager.pwd_context.hash(plaintext_password)


def verify_password(password_input: str, hashed_password: str):
    """ Check if the given password matches """
    return manager.pwd_context.verify(password_input, hashed_password)
