from typing import Optional
from sqlalchemy.orm import Session
from db.models import models
from db.models.models import User
from login_manager.login_manager import hash_password, manager
from schemas.user import UserCreate
from services.db_context import DBContext, get_db


class CRUDUser:

    def __init__(self):
        self.db = get_db()

    @staticmethod
    @manager.user_loader
    def get_by_email(email: str) -> Optional[User]:
        with DBContext() as db:
            return db.query(models.User).filter(models.User.email == email).first()

    def create(self, *, user: UserCreate) -> User:
        user_data = user.dict()
        user_data["password"] = hash_password(user.password)
        db_user = User(**user_data)
        self.add_and_commit(db_user)
        return db_user

    def add_and_commit(self, obj):
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)


user_crud = CRUDUser()
