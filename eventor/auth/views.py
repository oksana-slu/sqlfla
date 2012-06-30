# -*- encoding: utf-8 -*-
from flask import g, render_template
from flask.ext.security import login_required
from eventor.core.utils import jsonify_status_code

from . import auth
from eventor.auth.models import User


@auth.route('/')
@auth.route('/<int:id>')
@login_required
def profile(id=None):
    if id and g.user.has_roles('admin'):
        user = User.query.get_or_404(id)
    else:
        user = g.user
    return render_template("auth/show.html", profile=user)


@auth.route('/<email>')
def check_email(email):
    response = {'email_in_db': 'false'}
    user = User.query.filter_by(email=email).first()

    if user:
        response = {'email_in_db': 'true'}

    return jsonify_status_code(response)
