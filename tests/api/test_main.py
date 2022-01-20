# from fastapi.testclient import TestClient
# from app import application
# from tests.api.test_base import TestHelper


class TestApiE2e:
    def test_create_new_user(self, test_helper):
        create_new_user = test_helper.post(path=test_helper.REGISTER_ENDPOINT, json=test_helper.body).json()

        assert create_new_user['status_code'] == 200, f'Expected response status code to be 200, instead got: {create_new_user["status_code"]}'
        assert create_new_user['status'] == 'SUCCESS', f'Expected response status code to be "SUCCESS", instead got: {create_new_user["status"]}'
        assert create_new_user['message'] == 'User registered successfully', f'Expected response message to be "registered successfully", instead got: {create_new_user["message"]}'
        return create_new_user

    def test_send_otp(self, test_helper):
        activate_endpoint = test_helper.ACTIVATE_ENDPOINT

        send_otp = test_helper.post(path=activate_endpoint, data=test_helper.body).json()
        assert send_otp['status_code'] == 200, f'Expected response status code to be 200, instead got: {send_otp["status_code"]}'
        assert send_otp['status'] == 'SUCCESS', f'Expected response status code to be "SUCCESS", instead got: {send_otp["status"]}'
        assert send_otp['message'] == 'OTP was sent successfully', f'Expected response message to be "OTP was sent successfully", instead got: {send_otp["message"]}'

    def test_send_otp_again_before_1_hour(self, test_helper):
        activate_endpoint = test_helper.ACTIVATE_ENDPOINT

        send_otp = test_helper.post(path=activate_endpoint, data=test_helper.body).json()
        assert send_otp['detail'] == 'Action blocked, try again in an hour', f'Expected response to be "Action blocked, try again in an hour", instead got {send_otp["detail"]}'

    def test_activate_new_user(self, test_helper):
        activate_endpoint = test_helper.ACTIVATE_ENDPOINT + '1111'

        activate_user = test_helper.post(path=activate_endpoint, data=test_helper.body).json()
        assert activate_user['status_code'] == 200, f'Expected response status code to be 200, instead got: {activate_user["status_code"]}'
        assert activate_user['status'] == 'SUCCESS', f'Expected response status code to be "SUCCESS", instead got: {activate_user["status"]}'
        assert activate_user['message'] == 'User activated successfully', f'Expected response message to be "User activated successfully", instead got: {activate_user["message"]}'
        return activate_user

    def test_user_login(self, test_helper):
        login = test_helper.post(path=test_helper.LOGIN_ENDPOINT, data=test_helper.body).json()

        assert login['status_code'] == 200, f'Expected response status code to be 200, instead got: {login["status_code"]}'
        assert login['status'] == 'SUCCESS', f'Expected response status code to be "SUCCESS", instead got: {login["status"]}'
        assert login['message'] == 'User logged in successfully', f'Expected response message to be "User logged in successfully", instead got: {login["message"]}'
        assert login['data'].get('access_token'), 'Expected response data to include access_token'
        assert login['data'].get('token_type'), 'Expected response data to include token_type'

        # Set the test_helper's headers
        test_helper.set_headers(login['data'].get('access_token'))
        return login

    def test_shorten_url_success(self, test_helper):
        shorten = test_helper.post(path=test_helper.SHORTEN_ENDPOINT, json=test_helper.URL_BODY, headers=test_helper.headers).json()

        assert shorten['status_code'] == 200, f'Expected response status code to be 200, instead got: {shorten["status_code"]}'
        assert shorten['status'] == 'SUCCESS', f'Expected response status code to be "SUCCESS", instead got: {shorten["status"]}'
        assert shorten['message'] == 'url shortened successfully', f'Expected response message to be "url shortened successfully", instead got: {shorten["message"]}'

        assert shorten['data']['available_clicks'] == -1
        return shorten

    def test_shorten_url_with_invalid_date(self, test_helper):
        shorten = test_helper.post(path=test_helper.SHORTEN_ENDPOINT, json=test_helper.URL_BODY_WITH_INVALID_DATE, headers=test_helper.headers).json()
        assert shorten['detail'][0]['msg'] == 'date must be greater than current date'

# def test_helper():
#     base_url = 'http://127.0.0.1:8080'
#     client = TestClient(application)
#     test_helper = TestHelper(client=client, base_url=base_url)
#     return test_helper
#
#
# test = TestApiE2e()
# test_helper = test_helper()
#
# res = test.test_create_new_user(test_helper)
# print(res)
#
# res = test.test_activate_new_user(test_helper)
# print(res)
#
# res = test.test_user_login(test_helper)
# print(res)
#
# res = test.test_shorten_url_success(test_helper)
# print(res)
