from typing import Optional
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.param_functions import Form


class ExtendedOAuth2PasswordRequestForm(OAuth2PasswordRequestForm):
    """
    this class is used to extend OAuth2PasswordRequestForm so it will contain an email field
    """

    def __init__(self,
                 grant_type: str = Form(None, regex="password"),
                 username: Optional[str] = Form(None),
                 password: str = Form(...),
                 scope: str = Form(""),
                 client_id: Optional[str] = Form(None),
                 client_secret: Optional[str] = Form(None),
                 email: str = Form(...)):

        super().__init__(
            grant_type,
            username,
            password,
            scope,
            client_id,
            client_secret,
        )
        self.email = email
