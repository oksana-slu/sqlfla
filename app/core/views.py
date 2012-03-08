from flask import render_template
from flask.views import MethodView
from . import core


def register_api(url, name, key, ktype, bp):

    def closure(view):
        view_func = view.as_view(name)
        bp.add_url_rule(url, methods=['GET', 'POST'], view_func=view_func)
        bp.add_url_rule("%s<%s:%s>" % (url, ktype.__name__, key),
                methods=['GET', 'PUT', 'DELETE'], view_func=view_func)
    return closure


@register_api('/pages/', 'core_api', 'id', int, core)
class BaseView(MethodView):

    def get(self, id=None):
        return "get: %s" % id

    def post(self):
        return "post"

    def put(self, id):
        return "put: %s" % id

    def delete(self, id):
        return "delete: %s" % id


@core.route("/")
def index():
    return render_template("base.html", **{})
