# -*- encoding: utf-8 -*-
from flask import abort, render_template, current_app
from jinja2.exceptions import TemplateNotFound

from . import core
# from .models import Page


@core.route("/")
def index():
    return render_template('base.html')


@core.route('/login')
def login():
    return render_template('auth/login.html')


@core.route('/templates/<path:template>')
@core.route('/templates/')
def template(template=None):
    template or abort(404)

    try:
        return render_template(current_app.jinja_env.get_template(template))
    except TemplateNotFound:
        abort(404)


# @core.route("/page/<slug>")
# def page(slug):
#     page = Page.query.filter_by(slug=slug).first_or_404()
#     if page.auth_required and g.user.is_anonymous():
#         abort(403)
#     return render_template("page.html", page=page)
