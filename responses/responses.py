from starlette.responses import JSONResponse


class ApiResponse:

    def __init__(self):
        self.status_code = None

    @staticmethod
    def _response_builder(**kwargs):
        """
        Used to build an API response.
        """
        status = None
        status_code = kwargs.get('status_code')

        if status_code and str(status_code).startswith('4'):
            status = 'ERROR'
        elif status_code and str(status_code).startswith('2'):
            status = 'SUCCESS'

        response_body = {'status_code': status_code,
                         'status': status,
                         'message': kwargs.get('message') if kwargs.get('message') else None,
                         'data': kwargs.get('data')}

        return JSONResponse(status_code=status_code, content=response_body)

    def get_response(self, response_message=None, **kwargs):
        return self._response_builder(message=getattr(self.__class__, response_message) if response_message else None,
                                      data=kwargs.get('data'),
                                      status_code=self.status_code)


class SuccessResponses(ApiResponse):
    OTP_SENT_SUCCESSFUL = 'OTP was sent successfully'
    USER_ACTIVATED_SUCCESSFUL = 'User activated successfully'
    USER_REGISTERED_SUCCESSFUL = 'User registered successfully'
    USER_LOGGED_IN_SUCCESSFUL = 'User logged in successfully'
    URL_SHORTENED_SUCCESSFUL = 'url shortened successfully'

    def __init__(self):
        ApiResponse.__init__(self)
        self.status_code = 200


class ErrorResponses(ApiResponse):
    URL_EXPIRED = 'url is expired'
    WRONG_OTP = 'Wrong OTP provided'
    URL_NOT_EXIST = 'url does not exist'
    USER_NOT_ACTIVATED = 'User is not activated'
    USER_ALREADY_ACTIVATED = 'User is already activated'
    USER_ALREADY_EXIST = 'A user with this email already exists'

    def __init__(self):
        ApiResponse.__init__(self)
        self.status_code = 400


success_responses = SuccessResponses()
error_responses = ErrorResponses()
