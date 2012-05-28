import base64
import random

from datetime import datetime
from time import mktime

from sqlalchemy.ext.hybrid import hybrid_property

from eventor import app, db

from core.models import CRUDMixin
from core.utils import get_hexdigest
# from sqlalchemy import


class User(db.Model, CRUDMixin):
    """ By default model inherits id and created_at fields from the CRUDMixin
    """
    email = db.Column(db.String(80), unique=True, index=True)
    _password = db.Column(db.String(512))
    first_name = db.Column(db.Unicode(255))
    last_name = db.Column(db.Unicode(255))
    phone = db.Column(db.String(15))
    is_superuser = db.Column(db.Boolean, default=False)
    logged_at = db.Column(db.DateTime, default=datetime.utcnow,
                          onupdate=datetime.utcnow)

    def __repr__(self):
        return "<User: %r>" % self.email

    @classmethod
    def create(cls, **kwargs):
        # FYI: user is never created with the password set by hands.
        # We should change it only through the account activation.
        kwargs['password'] = '*'
        kwargs['is_superuser'] = kwargs['email'] in app.config['ADMINS']

        return cls(**kwargs).save()

    @classmethod
    def authenticate(cls, email, password):
        user = cls.query.filter_by(email=email.lower()).first()
        if user is not None:
            salt, hsh = user.password.split('$')
            # TODO: understand password checking
            if hsh == get_hexdigest(salt, password):
                return user
        return user

    @classmethod
    def is_unique(cls, email):
        return cls.query.filter_by(email=email).count() == 0

    @classmethod
    def validate_token(cls, token=None):
        if token is not None and '$$' in token:
            key, hsh = token.split('$$')
            user = cls.query.filter_by(email=base64.decodestring(key)).first()
            if user and token == user.create_token():
                return user
        return None

    def create_token(self):
        """ creates a unique token based on user last login time and
        urlsafe encoded user key
        """
        ts_datetime = self.logged_at or self.created_at
        ts = int(mktime(ts_datetime.timetuple()))
        key = base64.encodestring(self.email).rstrip('\n\r ')
        base = "{}{}".format(key, ts)
        salt, hsh = self.password.split('$')
        return "{}$${}".format(key, get_hexdigest(salt, base))

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password_setter(self, value):
        rand_str = lambda: str(random.random())
        salt = get_hexdigest(rand_str(), rand_str())[:5]
        hsh = get_hexdigest(salt, value)
        self._password = '{}${}'.format(salt, hsh)

    @property
    def full_name(self):
        full_name = " ".join([self.first_name or '', self.last_name or ''])
        return full_name.strip() or self.email
