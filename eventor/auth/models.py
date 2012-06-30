# -*- encoding: utf-8 -*-
from sqlalchemy.ext.associationproxy import association_proxy

from flask.ext.security import Security, UserMixin
from flask.ext.security.datastore import SQLAlchemyUserDatastore

from eventor import app, db

from eventor.core.models import CRUDMixin
# from sqlalchemy import

users_roles = db.Table('users_roles', db.metadata,
        db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
        db.Column('roles_id', db.Integer, db.ForeignKey('roles.id')),
)


class User(db.Model, CRUDMixin, UserMixin):
    """ By default model inherits id and created_at fields from the CRUDMixin
    """
    email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(512), nullable=False)
    first_name = db.Column(db.Unicode(255))
    last_name = db.Column(db.Unicode(255))
    phone = db.Column(db.String(15))
    active = db.Column(db.Boolean, default=False)

    confirmation_token = db.Column(db.String(255))
    confirmation_sent_at = db.Column(db.DateTime())
    confirmed_at = db.Column(db.DateTime())

    reset_password_token = db.Column(db.String(255))
    reset_password_sent_at = db.Column(db.DateTime())

    authentication_token = db.Column(db.String(255))
    authentication_token_created_at = db.Column(db.DateTime())

    roles = db.relationship('Role', secondary=users_roles, lazy='dynamic',
                            backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return "<User: %r>" % self.email

    @classmethod
    def create(cls, **kwargs):
        return app.security.datastore.create_user(**kwargs)

    @classmethod
    def is_unique(cls, email):
        return cls.query.filter_by(email=email).count() == 0

    @property
    def full_name(self):
        full_name = " ".join([self.first_name or '', self.last_name or ''])
        return full_name.strip() or self.email


class Role(db.Model, CRUDMixin):
    name = db.Column(db.Unicode(255), nullable=False, unique=True)

    @classmethod
    def get_or_create(cls, name):
        return cls.query.filter_by(name=name).first() or cls.create(name=name)


Security(app, SQLAlchemyUserDatastore(db, User, Role))
