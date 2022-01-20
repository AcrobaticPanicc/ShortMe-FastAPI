from db.models import models
from login_manager.login_manager import hash_password
from services.db_context import DBContext, get_db


class CRUDUrl:

    def __init__(self):
        self.db = get_db()

    def shorten_url(self,
                    owner_id,
                    long_url,
                    available_clicks=None,
                    expires_at=None,
                    is_active=True,
                    password=None,
                    custom_url=None
                    ):
        if password:
            password = hash_password(password)

        short_url = models.ShortUrl(long_url=long_url,
                                    owner_id=owner_id,
                                    available_clicks=available_clicks,
                                    expires_at=expires_at,
                                    is_active=is_active,
                                    password=password,
                                    custom_url=custom_url
                                    )

        self.add_and_commit(short_url)
        return short_url

    def get_url(self, short_url: str):
        return self.db.query(models.ShortUrl).filter(models.ShortUrl.short_url == short_url).first()

    def get_urls(self, owner_id: int):
        return self.db.query(models.ShortUrl).filter(models.ShortUrl.owner_id == owner_id).all()

    def add_and_commit(self, obj):
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)


url_crud = CRUDUrl()
