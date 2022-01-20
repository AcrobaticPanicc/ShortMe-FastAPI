import time
import requests
from datetime import datetime


class Date(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, date):
        """
        Validates that the given date follows the following pattern: "dd:mm:yyyy hh:mm"
        :param date: str
        :return: date given date in unix format
        """
        if not isinstance(date, str):
            raise TypeError('Date must be a string')

        date_to_unix = None
        format_string = "%d/%m/%Y %H:%M"
        try:
            date_to_unix = datetime.strptime(date, format_string).timestamp()

        except ValueError:
            raise ValueError('invalid date format, make sure to use dd/mm/yyyy hh:mm')

        finally:
            cls.validate_date(date_to_unix)

        return date_to_unix

    @staticmethod
    def validate_date(unix_time):
        """
        Validates that the given unix time is greater than the current time
        :param unix_time:
        :return: unix_time
        """
        time_now = time.time()

        if unix_time:
            if time_now < unix_time:
                return unix_time
            raise ValueError('date must be greater than current date')


class Url(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, url):
        """
        Validates that a given url is valid
        :param url:
        :return:
        """
        if not isinstance(url, str):
            raise TypeError('string required')

        url = url if url.startswith('http') else ('http://' + url)

        try:
            res = requests.get(url)
            return res.url

        except requests.exceptions.ConnectionError:
            raise TypeError('connection error - there was no response from given url')

        except requests.exceptions.InvalidURL:
            raise TypeError('invalid url - please check the given url and try again')

        except:
            raise TypeError('uknown error occurred')


class CustomUrl(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, custom_url):
        """
        Validates that a given custom url is not longer than 10 characters or shorter than 5 characters
        :param custom_url: str
        :return:
        """
        if not isinstance(custom_url, str):
            raise TypeError('string required')

        if len(custom_url) < 5 or len(custom_url) > 10:
            raise ValueError('url length must be between 5 and 10 characters')

        return custom_url
