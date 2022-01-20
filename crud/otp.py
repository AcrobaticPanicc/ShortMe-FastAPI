from db.models import models
from crud.user import user_crud
from services.db_context import get_db


class CRUDOtp:

    def __init__(self):
        self.db = get_db()

    def create_otp(self, email: str):
        """
        create a new otp code or removing the old verification code an creating a new one
        """
        user = user_crud.get_by_email(email)
        user_id = user.id_

        # delete old verification code if exists
        otp = self.db.query(models.Otp).filter(models.Otp.user_id == user.id_)
        if otp:
            otp.delete()

        return self.get_otp(user_id)

    def get_otp(self, user_id: int):
        new_otp = models.Otp(user_id=user_id)
        self.add_and_commit(new_otp)
        return new_otp

    def add_and_commit(self, obj):
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)


otp_crud = CRUDOtp()
