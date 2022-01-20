from fastapi import APIRouter, HTTPException, Request
from fastapi import Depends
from crud.otp import otp_crud
from crud.user import user_crud
from responses.responses import error_responses, success_responses
from services.email import send_email_async
from services.extended_oauth2 import ExtendedOAuth2PasswordRequestForm
from services.limiter import limiter
from services.user_validator import validate_user

router = APIRouter()


@router.post("/user/activate/{otp}")
async def activate(otp, data: ExtendedOAuth2PasswordRequestForm = Depends()):
    """
    User activation route.

    Args:
        otp (str): The OTP (one time password) sent to the user over the given email
        data (ExtendedOAuth2PasswordRequestForm): The user object sent in the request

    Returns:
        USER_ACTIVATED_SUCCESSFUL response object with data:
            "email": user.email,
            "is_active": user.is_active,
            "full_name": user.full_name

    Raises:
        - Error USER_ALREADY_ACTIVATED if the user is already activated
        - Error WRONG_OTP if the given OTP does not match the stored OTP

    """
    user = validate_user(data)

    if user.is_active:
        return error_responses.get_response('USER_ALREADY_ACTIVATED', data={'user': user.email})

    user_otp = otp_crud.get_otp(user.id_)

    if user_otp.otp == otp:
        user.is_active = True
        user_crud.add_and_commit(user)

        data = {
            "email": user.email,
            "is_active": user.is_active,
            "full_name": user.full_name
        }

        return success_responses.get_response('USER_ACTIVATED_SUCCESSFUL', data=data)

    else:
        return error_responses.get_response('WRONG_OTP')


@router.post("/user/activate/")
@limiter.limit("1/hour", error_message='Action blocked, try again in an hour')
async def get_new_otp(request: Request, data: ExtendedOAuth2PasswordRequestForm = Depends()):
    """
    A route used for sending a new OTP over the email to the given user.

    Args:
        request (Request): A request obj
        data (ExtendedOAuth2PasswordRequestForm): The user object sent in the request

    Returns:
        OTP_SENT_SUCCESSFUL response

    Raises:
        - Error USER_ALREADY_ACTIVATED if the user is already activated

    """
    user = validate_user(data)

    if user.is_active:
        return error_responses.get_response('USER_ALREADY_ACTIVATED', data={'user': user.email})

    new_otp = otp_crud.create_otp(user.email)
    await send_email_async("Your OTP", user.email, new_otp)

    data = {"email": user.email}
    return success_responses.get_response('OTP_SENT_SUCCESSFUL', data=data)
