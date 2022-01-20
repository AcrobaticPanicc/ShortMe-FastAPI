import datetime as _dt
import string
from random import choices, randint
import sqlalchemy as sql
import sqlalchemy.orm as orm
from db import database
from services import db_context


class User(database.Base):
    __tablename__ = "users"
    id_ = sql.Column(sql.Integer, primary_key=True, index=True)
    email = sql.Column(sql.String, unique=True, index=True)
    password = sql.Column(sql.String)
    is_active = sql.Column(sql.Boolean, default=False)
    full_name = sql.Column(sql.String, default=None)

    short_urls = orm.relationship("ShortUrl", back_populates="owner")


class ShortUrl(database.Base):
    __tablename__ = "short_urls"
    id_ = sql.Column(sql.Integer, primary_key=True, index=True)
    owner_id = sql.Column(sql.Integer, sql.ForeignKey("users.id_"))
    long_url = sql.Column(sql.String, index=True)
    short_url = sql.Column(sql.String, unique=True)
    password = sql.Column(sql.String)
    expires_at = sql.Column(sql.String)
    custom_url = sql.Column(sql.String, default=None)
    visits = sql.Column(sql.Integer, default=0)
    available_clicks = sql.Column(sql.Integer, default=-1)
    is_active = sql.Column(sql.Boolean, default=True)
    date_created = sql.Column(sql.DateTime, default=_dt.datetime.utcnow)
    owner = orm.relationship("User", back_populates="short_urls")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.short_url = self.generate_short_url() if not self.short_url else self.short_url

    def __repr__(self):
        return f'short_url: {self.short_url} id: {self.id_}'

    def generate_short_url(self):
        characters = string.digits + string.ascii_letters
        short_url = ''.join(choices(characters, k=5))

        with db_context.DBContext() as db:
            url = db.query(ShortUrl).filter(ShortUrl.short_url == short_url).first()

            if url:
                return self.generate_short_url()

        return short_url


class Otp(database.Base):
    __tablename__ = 'otp'
    id_ = sql.Column(sql.Integer, primary_key=True)
    user_id = sql.Column(sql.Integer, sql.ForeignKey('users.id_'))
    otp = sql.Column(sql.String(7))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.otp = self.generate_otp()
        self.otp = 1111  # <<< for testing

    @staticmethod
    def generate_otp():
        otp = ' '.join([str(randint(0, 999)).zfill(3) for _ in range(2)])
        return otp

    def __repr__(self):
        return f'{self.otp}'
