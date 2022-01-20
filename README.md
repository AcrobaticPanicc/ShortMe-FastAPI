# ShortMe
###URL Shortener API with many features for links shortening. 

<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About The Project](#about)
    + [How it Works](#How-it-Works)
+ [Built With](#built-with)
    + [Extensions](#extensions)
+ [Run locally](#run-locally)
+ [Features](#features)
+ [Usage](#usage)


<!-- about -->
## About the project

### ShortMe API
An asynchronous API service built using FastAPI, used to shorten long URLs.

<!-- How-it-Works -->
#### How it works
When submitting a URL, it goes through a validity check and added http:// prefix in case it was not provided.
Once done, a random base64 string is generated and added to an SQLite database with the submitted corresponding URL.
The user is then given a short URL formatted like so: WEBSITE_DOMAIN/token, the token being the base 64 string.
Whenever this unique URL is visited, the user will get redirected automatically to the corresponding URL in the database.

<!-- built-with -->
#### Built with
* [FastAPI](https://fastapi.tiangolo.com/) - Backend

<!-- extensions -->
#### Extensions
* [FastAPI Login](https://fastapi-login.readthedocs.io/) - User authentication
* [Fastapi-mail](https://sabuhish.github.io/fastapi-mail/) - Mail
* [FastAPI-SQLAlchemy](https://pypi.org/project/FastAPI-SQLAlchemy/) - SQL ORM
* [slowapi](https://pypi.org/project/slowapi/) - API rate limiter
* [Pytest](https://docs.pytest.org/) - Testing

<!-- run-locally -->
## Run Locally
Clone using

    $ git clone https://github.com/AcrobaticPanicc/ShortMe-FastAPI.git

Create a virtual environment for the project and activate it:

    $ virtualenv venv
    $ source venv/bin/activate

Install the required packages:

    $ pip install -r requirements.txt

Run the app using:

    $ python app.py

<!-- features -->
### Features
ShortMe API is packed with some neat features:
* User registration and authentication
* Protect a URL with password
* Activate or deactivate a URL
* Set amount of total clicks
* Set experation date
* Set a custom short url (wip) 

<!-- usage -->
#### Usage
In order for a user to use the API, the user needs to register using an email address, activate the email address, and log in. 

#### Flow:

##### Register:

###### Request:

```python
import requests
import json

url = "http://127.0.0.1:8080/user/register"

payload = json.dumps({
  "email": "user@email.com",
  "password": 1234
})

headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
```

###### Response:

```
{
    "status_code": 200,
    "status": "SUCCESS",
    "message": "User registered successfully",
    "data": {
        "email": "user@email.com",
        "full_name": null
    }
}
``` 

##### Activate:

###### Request:

```python
import requests

url = "http://127.0.0.1:8080/user/activate/{otp}"

payload = {'email': 'user@email.com',
           'password': '1234'}

response = requests.request("POST", url, data=payload)

print(response.text)

```

###### Response:

```
{
    "status_code": 200,
    "status": "SUCCESS",
    "message": "User activated successfully",
    "data": {
        "email": "user@email.com",
        "is_active": true,
        "full_name": null
    }
}
``` 

##### Login:

###### Request:

```python
import requests

url = "http://127.0.0.1:8080/user/token"

payload = {'email': 'user@email.com',
'password': '1234'}

response = requests.request("POST", url, data=payload)

print(response.text)

```

###### Response:

```
{
    "status_code": 200,
    "status": "SUCCESS",
    "message": "User logged in successfully",
    "data": {
        "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ0b21lckBnbWFpbC5jb20iLCJleHAiOjE2NDI2NzI2OTN9.IbmP8QR1KnQyXCuxZUfbWDCa8-MJyYDcbdDf-bYEQ3g",
        "token_type": "Bearer"
    }
}
``` 

##### Shorten:

###### Request:

```python
import requests
import json

url = "http://127.0.0.1:8080/shorten"

payload = json.dumps({
  "long_url": "www.youtube.com",
  "expires_at": "12/12/2022 23:23",
  "password": 1234
})
headers = {
  'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ0b21lckBnbWFpbC5jb20iLCJleHAiOjE2NDI2NzI2OTN9.IbmP8QR1KnQyXCuxZUfbWDCa8-MJyYDcbdDf-bYEQ3g',
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)


```

###### Response:
```
{
    "status_code": 200,
    "status": "SUCCESS",
    "message": "url shortened successfully",
    "data": {
        "long_url": "https://www.youtube.com/",
        "is_active": true,
        "password": "1234",
        "available_clicks": -1,
        "expires_at": "1670880180.0",
        "custom_url": null,
        "short_url": "http://127.0.0.1:8080/AF36a",
        "date_created": "2022-01-20 09:46:07.296924"
    }
}
```
