# -*- encoding: utf-8 -*-
from sqlalchemy.ext.hybrid import hybrid_property

from eventor import db
from eventor.core.models import CRUDMixin
from eventor.core.utils import plural_name, underscorize


def api_resource(bp, endpoint, pk_def):
    pk = pk_def.keys()[0]
    pk_type = pk_def[pk] and pk_def[pk].__name__ or None
    # building url from the endpoint
    url = "/{}/".format(endpoint)

    def wrapper(resource_class):
        resource = resource_class().as_view(endpoint)
        bp.add_url_rule(url, view_func=resource, methods=['GET', 'POST'])
        if pk_type is None:
            url_rule = "%s<%s>" % (url, pk)
        else:
            url_rule = "%s<%s:%s>" % (url, pk_type, pk)
        bp.add_url_rule(url_rule,
                        view_func=resource,
                        methods=['GET', 'PUT', 'DELETE'])
        return resource_class

    return wrapper


def multilingual(cls):

    def closure(cls):
        class_name = cls.__name__ + 'Localized'
        tablename = plural_name(underscorize(class_name))
        if db.metadata.tables.get(tablename) is not None:
            return
        # TODO: pass language from the babel detection
        lang = u'en'
        cls_columns = cls.__table__.get_children()
        columns = dict([(c.name, c.copy()) for c in cls_columns if isinstance(c.type, (db.Unicode, db.UnicodeText))])
        localized_names = columns.keys()
        columns.update({
            'parent_id': db.Column(db.Integer, db.ForeignKey(cls.__tablename__ + '.id'), nullable=False),
            'parent': db.relationship(cls, backref='localized_ref'),
            'locale': db.Column(db.Unicode(255), default=lang, index=True)
        })

        cls_localized = type(class_name, (db.Model, CRUDMixin), columns)

        for field in localized_names:

            def getter(self):
                localized = cls_localized.query.filter_by(parent_id=self.id, locale=lang).first()
                return getattr(localized, field) or None

            def setter(self, value):
                localized = cls_localized.query.filter_by(parent_id=self.id, locale=lang).first() or cls_localized(parent=self, locale=lang)
                setattr(localized, field, value)
                localized.save()

            def expression(self):
                return db.Query(columns[field]).filter(cls_localized.parent_id == self.id, cls_localized.locale == lang).as_scalar()

            setattr(cls, field, hybrid_property(getter, setter, expr=expression))

        closure(cls)

    return cls
