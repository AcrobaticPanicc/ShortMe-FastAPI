from fastapi import APIRouter
from fastapi import Depends
from login_manager.login_manager import manager
from responses.responses import success_responses, error_responses
from services.extended_oauth2 import ExtendedOAuth2PasswordRequestForm
from services.user_validator import validate_user
from setup.settings import settings

router = APIRouter()


@router.post(settings.token_url)
async def login(data: ExtendedOAuth2PasswordRequestForm = Depends()):
    """
    A route used to login a user.

    Args:
        data (ExtendedOAuth2PasswordRequestForm): The user object sent in the request

    Returns:
        USER_LOGGED_IN_SUCCESSFUL response containing the access token and the token type:
            {'access_token': access_token,
            'token_type': 'Bearer'}

    Raises:
        - Error USER_NOT_ACTIVATED if the user is not activated

    """
    user = validate_user(data)

    if not user.is_active:
        return error_responses.get_response('USER_NOT_ACTIVATED')

    access_token = manager.create_access_token(data=dict(sub=user.email))

    data = {
        'access_token': access_token,
        'token_type': 'Bearer'
    }

    return success_responses.get_response('USER_LOGGED_IN_SUCCESSFUL', data=data)


