from fastapi_login.exceptions import InvalidCredentialsException
from crud.user import user_crud
from login_manager.login_manager import verify_password
from services.extended_oauth2 import ExtendedOAuth2PasswordRequestForm


def validate_user(data: ExtendedOAuth2PasswordRequestForm):
    """
    This function is used to validate a user credentials and return
    the user obj from db if all the credentials are valid.
    :param data: an ExtendedOAuth2PasswordRequestForm obj containing the user credentials
    :return: user db object
    """
    email = data.email
    password = data.password

    user = user_crud.get_by_email(email)

    if user is None:
        raise InvalidCredentialsException

    elif not verify_password(password, user.password):
        raise InvalidCredentialsException

    return user
