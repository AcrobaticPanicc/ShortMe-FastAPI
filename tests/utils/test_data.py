class TestData:
    URL_BODY = {
        "long_url": 'www.youtube.com',
        'expires_at': '12/12/2022 23:23',
    }

    URL_BODY_WITH_AVAILABLE_CLICKS = {
        "long_url": 'www.youtube.com',
        'available_clicks': 2,
        'expires_at': '12/12/2021 23:23',
        'password': '1234'
    }

    URL_BODY_WITH_INVALID_DATE = {
        "long_url": 'www.youtube.com',
        'expires_at': '12/12/2000 23:23',
    }

    URL_BODY_WITH_INVALID_URL = {
        "long_url": '***',
        'expires_at': '12/12/2022 23:23',
    }
