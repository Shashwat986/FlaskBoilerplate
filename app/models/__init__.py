from app import db
from sqlalchemy_mixins import AllFeaturesMixin

class SQLBase(db.Model, AllFeaturesMixin):
    __abstract__ = True

    def save(self):
        try:
            super().save()
            self.session.commit()
        except:
            self.session.rollback()
            raise

    def delete(self):
        try:
            super().delete()
            self.session.commit()
        except:
            self.session.rollback()
            raise

SQLBase.set_session(db.session)
