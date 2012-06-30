# -*- encoding: utf-8 -*-
from datetime import datetime

from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.hybrid import hybrid_property

from flask.ext.sqlalchemy import orm

from eventor import db
from eventor.core.utils import plural_name, slugify, underscorize


def raise_value(text):
    raise ValueError(text)


class CRUDMixin(object):
    """ Basic CRUD mixin
    """
    __table_args__ = {'extend_existing': True,
                      'mysql_charset': 'utf8',
                      'mysql_engine': 'InnoDB'}

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @declared_attr
    def __tablename__(cls):
        """ We want our app to be more English for pluralization cases
        """
        return plural_name(underscorize(cls.__name__))

    @classmethod
    def get(cls, id):
        return cls.query.get(id)

    @classmethod
    def create(cls, **kwargs):
        return cls(**kwargs).save()

    def update(self, commit=True, **kwargs):
        return self.__setattrs(**kwargs).save(commit)

    def save(self, commit=True):
        db.session.add(self)
        commit and db.session.commit()
        return self

    def delete(self, commit=True):
        db.session.delete(self)
        commit and db.session.commit()

    def __setattrs(self, **kwargs):
        for key in kwargs:
            key.startswith('_') and raise_value('Underscored values are not allowed')
            try:
                getattr(self, key)
                setattr(self, key, kwargs[key])
            except AttributeError:
                continue

        return self

    def as_dict(self, exclude=['password']):
        """ method for building dictionary for model value-properties filled
            with data from mapped storage backend
        """
        # columns = self._sa_class_manager
        # relations = [k for k in columns if isinstance(columns[k].property, orm.properties.RelationshipProperty)]
        columns = (p.key for p in self.__mapper__.iterate_properties if isinstance(p, orm.ColumnProperty))
        response = {}
        for col_name in columns:
            regular_name = col_name.startswith('_') and col_name[1:] or col_name
            response[regular_name] = regular_name not in exclude and getattr(self, regular_name)

        return response


class SlugMixin(CRUDMixin):
    """Basic mixin for models with slug and name
    """
    name = db.Column(db.Unicode(512), nullable=False)
    _slug = db.Column(db.String(128), nullable=False, unique=True)

    @hybrid_property
    def slug(self):
        return self._slug

    @slug.setter
    def slug(self, name):
        self._slug = slugify(name)

    def save(self, commit=True):
        self.slug = self.name
        return super(SlugMixin, self).save(commit)

    @classmethod
    def get_by_slug(cls, slug):
        return cls.query.filter_by(slug=slug).first()

    def __repr__(self):
        return "<%s:%s>" % (self.__class__.__name__,
                            self.name)


class Page(db.Model, SlugMixin):
    content = db.Column(db.UnicodeText)
    auth_required = db.Column(db.Boolean, default=False, nullable=False)
