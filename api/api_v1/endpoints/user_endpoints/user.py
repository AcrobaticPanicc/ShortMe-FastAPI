from fastapi import APIRouter, Depends
from crud.url import url_crud
from login_manager.login_manager import manager
from responses.responses import success_responses, error_responses
from schemas.url import UrlResponse
from schemas.user import UserResponse
from services.extended_oauth2 import ExtendedOAuth2PasswordRequestForm

router = APIRouter()


@router.get("/user")
async def user(user=Depends(manager)):
    """
    A route used to retrieve all given user's information.

    Args:
        user (UserCreate): an object containing the user details

    Returns:
        response containing the given user's information:
            {'id': user.id_,
            'email': user.email,
            'is_active': user.is_active,
            'short_urls': urls}

    Raises:
        - Error USER_ALREADY_EXIST if a user with this email already exists.

    """
    db_urls = url_crud.get_urls(user.id_)

    urls = [UrlResponse(
        expires_at=url.expires_at,
        short_url=url.short_url,
        date_created=str(url.date_created),
        long_url=url.long_url
    ).dict() for url in db_urls]

    data = {'id': user.id_,
            'email': user.email,
            'is_active': user.is_active,
            'short_urls': urls
            }

    return success_responses.get_response(data=data)
