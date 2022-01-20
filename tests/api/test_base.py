import json
import random
from starlette.testclient import TestClient
from app import application
from tests.utils.endpoints import Endpoints
from tests.utils.http_request import HttpRequest
from tests.utils.test_data import TestData


class TestHelper(HttpRequest, Endpoints, TestData):
    __test__ = False
    RANDOM_STR = "".join([str(random.randint(1, 10)) for x in range(1, 10)])

    def __init__(self, *, email=None, client, base_url):
        super().__init__(base_url=base_url, client=client)

        self.test_client = client
        self.access_token = None
        self.headers = None

        self.email = email
        if not email:
            self.email = f'{self.RANDOM_STR}@gmail.com'

        self.body = {
            "email": self.email,
            "password": 1234
        }

    def set_headers(self, access_token: str) -> None:
        self.headers = {
            "Authorization": f'Bearer {access_token}'
        }