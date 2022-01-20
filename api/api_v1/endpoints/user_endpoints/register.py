from fastapi import APIRouter, HTTPException
from crud.user import user_crud
from crud.otp import otp_crud
from responses.responses import success_responses, error_responses
from schemas.user import UserCreate
from services.email import send_email_async

router = APIRouter()


@router.post("/user/register")
async def register(user: UserCreate):
    """
    A route used to register a user.
    Sending an email to the user's email with a OTP.

    Args:
        user (UserCreate): an object containing the user details

    Returns:
        USER_REGISTERED_SUCCESSFUL response containing the new user's information:
            {'email': user.email,
            'full_name': user.full_name}

    Raises:
        - Error USER_ALREADY_EXIST if a user with this email already exists.

    """

    if user_crud.get_by_email(email=user.email) is not None:
        return error_responses.get_response('USER_ALREADY_EXIST')

    else:
        db_user = user_crud.create(user=user)
        otp = otp_crud.create_otp(db_user.email)
        await send_email_async('test subject', user.email, otp)
        # todo: add a meaningful message
        data = {
            'email': user.email,
            'full_name': user.full_name,
            # 'is_active': user.is_active,
        }
        return success_responses.get_response('USER_REGISTERED_SUCCESSFUL', data=data)


"""
------------------------------------------------------
REGISRATION FLOW
------------------------------------------------------

user send POST with email and password to /user/register
    
    case user exist:
        return 400, email address is already in use
    
    case user not exist:
        create user, is_active = False, create otp, send otp over email

------------------------------------------------------
ACTIVATION FLOW
------------------------------------------------------

user send OTP and username to /user/activate

    case OTP is valid and matches the email:
        change user's is_active to True, return success
    
    case OTP and/or email is not a match
        return failure 
    
    case user already activated:
        return error, "user already activated"

------------------------------------------------------
LOGIN FLOW
______________________________________________________

user send POST with email as username and password to /user/token

    case user is not activated:
        block action, alert that user must be activated
    
    case user is active:
        provide the Bearer token 


------------------------------------------------------
FORGOT PASSWORD FLOW
______________________________________________________
user send POST with email to /user/forgot 
    create a new otp -> otp is sent to user's email -> user 


"""









