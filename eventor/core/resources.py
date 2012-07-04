import trafaret as t

from functools import wraps

from flask import abort, request, g
from flask.views import MethodView

from flask.ext.security import login_required
from flask.ext.sqlalchemy import orm

from eventor import db

from . import http
from . import core
from .decorators import api_resource
from .utils import jsonify_status_code


class Resource(MethodView):

    method_decorators = None

    def dispatch_request(self, *args, **kwargs):
        """ Overriding MethodView dispatch call to decorate every
            method-related view-function with the method-related decorators
            declared as dictionary in the method_decorators class-value

            Sample:
            method_decorators = {
                'get': user_required,
                'post': [in_groups('manager'), check_superuser]}
        """
        method = super(Resource, self).dispatch_request

        if self.method_decorators is None:
            return method(*args, **kwargs)

        method_decorators = self.method_decorators.get(request.method.lower())

        if method_decorators:

            if isinstance(method_decorators, (list, tuple)):
                for decorator in method_decorators:
                    method = decorator(method)

            elif getattr(method_decorators, '__call__'):
                method = method_decorators(method)

        return method(*args, **kwargs)

    def get_objects(self, *args, **kwargs):
        """abstract method, must be implemented in subclasses,
        like method for extraction object list query
        """
        raise NotImplemented('Method is not implemented')

    def paginate(self, page=1, page_size=20, **kwargs):
        objects = self.get_objects(**kwargs)
        count = objects.count()
        pages = int(count / page_size) + (count % page_size and 1)
        page = page if page <= pages else pages
        page = page > 0 and page or 1
        items = objects.limit(page_size).offset((page - 1) * page_size)
        return items, count, pages, page

    def gen_list_response(self, **kwargs):
        """if response contains objects list, this method generates
        structure of response, with pagination, like:
            {'meta': { 'total': total objects,
                       'pages': amount pages},
                       'objects': objects list}
        """
        page = 'page' in request.args and int(request.args['page'])
        items, total, pages, page = self.paginate(page, **kwargs)
        response = {'meta': {
                            'total': total,
                            'pages': pages,
                            'page': page},
                    'objects': [self.model_as_dict(item) for item in items]}
        return response


class ModelResource(Resource):
    """ Resource for typical views
    """
    model = None
    # FIXME: self validation is None
    validation = t.Dict().allow_extra('*')
    include = ['id']

    def get(self, id=None):
        if id is None:
            response = self.gen_list_response()
        else:
            response = self.model_as_dict(self.get_object(id))

        return jsonify_status_code(response)

    def post(self):
        data = request.json or abort(http.BAD_REQUEST)
        status = http.CREATED
        try:
            data = self.validation.check(data)
            response = self.model_as_dict(self.model.create(**data))
        except t.DataError as e:
            status, response = http.BAD_REQUEST, e.as_dict()

        return jsonify_status_code(response, status)

    def put(self, id):
        data = request.json or abort(http.BAD_REQUEST)
        status = http.ACCEPTED
        try:
            data = self.validation.check(data)
            instance = self.get_object(id)
            response = self.model_as_dict(instance.update(**data))
        except t.DataError as e:
            status, response = http.BAD_REQUEST, e.as_dict()

        return jsonify_status_code(response, status)

    def delete(self, id):
        self.get_object(id).delete()
        return jsonify_status_code({}, http.NO_CONTENT)

    def get_objects(self):
        """ Method for extraction object list query
        """
        self.model is None and abort(http.BAD_REQUEST)
        return self.model.query

    def get_object(self, id):
        """ Method for extracting single object for requested id regarding
            on previous filters applied
        """
        return self.get_objects().filter_by(id=id).first_or_404()

    def model_as_dict(self, model):
        """ method for building dictionary for model value-properties filled
            with data from mapped storage backend
        """
        # columns = self._sa_class_manager
        # relations = [k for k in columns if isinstance(columns[k].property, orm.properties.RelationshipProperty)]
        mapper = model.__mapper__
        export_fields = super(self.__class__, self).include + self.include
        columns = (p.key for p in mapper.iterate_properties if isinstance(p, orm.ColumnProperty))
        response = {}
        for col_name in columns:
            if col_name in export_fields:
                regular_name = col_name.startswith('_') and col_name[1:] or col_name
                response[regular_name] = regular_name and getattr(model, regular_name)

        return response


class TableResource(Resource):
    """ Resource for views based on a table, witch is mapping M2M relation
        between users table and other object - related object.
        requires login user.
        The base table must have the same name as the backref to users,
        and the first row in the base table must be ForeignKey to 'id'
        of related object

        Sample:
            comments = Table('comment', db.metadata,
                db.Column('comment_id', db.Integer, db.ForeignKey('comments.id')),
                db.Column('user_id', db.Integer, db.ForeignKey('users.id')))

            class Comment(db.Model):
                id = db.Column(db.Integer, primary_key=True)
                ...
                comments_by  = db.relationship('User', secondary=comments
                                                 backref='comments')
    """

    table = None
    validation = t.Dict({'objects': t.List(t.Dict({'id': t.Int}))})\
                    .allow_extra('*')
    method_decorators = {'post': [login_required]}

    @property
    def columns(self):
        return [column.name for column in self.table.get_children()]

    @property
    def ref_column(self):
        return self.table.get_children()[0]

    def get(self):
        return jsonify_status_code(self.gen_list_response())

    def post(self):
        data = request.json or abort(http.BAD_REQUEST)
        status = http.CREATED

        try:
            objects = self.validation.check(data)['objects']

            insert_data = [dict(zip(self.columns, (item['id'], g.user.id))) for item in objects]

            response = db.engine.execute(self.table.insert(), insert_data)\
                        .last_inserted_params()
        except t.DataError as e:
            status, response = http.BAD_REQUEST, e.as_dict()

        return jsonify_status_code(response, status)

    def delete(self, id):
        status, response = http.NO_CONTENT, {}

        try:
            id = t.Int().check(id)
            db.engine.execute(self.table.delete().where(self.ref_column == id))

        except t.DataError as e:
            status, response = http.BAD_REQUEST, e.as_dict()

        return jsonify_status_code(response, status)

    def get_objects(self, **kwargs):
        ids = kwargs.pop('ids', None)
        query = getattr(g.user, self.table.fullname).filter_by(**kwargs)

        if isinstance(ids, (list, tuple)):
            query = query.filter(self.ref_column.in_(ids))

        return query


# --------- stuff for testing method-related decorators

def get_decorator(data):

    def wrap(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            response = func(*args, **kwargs)
            response.data = data
            return response

        return wrapper

    return wrap


@api_resource(core, 'fake', {'id': int})
class TestResource(Resource):

    method_decorators = {
        'get': get_decorator(data='modified response')
    }

    def get(self):
        return jsonify_status_code(**{'data': 'no data'})
