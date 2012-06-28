from flask import abort, g, render_template
from flask.ext.security import LoginForm, RegisterForm

from . import core
from .models import Page


@core.route("/")
def index():
    return render_template('base.html', sign_in_form=LoginForm(),
                           sign_up_form=RegisterForm())


@core.route("/page/<slug>")
def page(slug):
    page = Page.query.filter_by(slug=slug).first_or_404()
    if page.auth_required and g.user.is_anonymous():
        abort(403)
    return render_template("page.html", **page.as_dict())
