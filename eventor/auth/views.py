# -*- encoding: utf-8 -*-
from flask import g, render_template
from flask.ext.security import login_required


from . import auth
from .models import User


@auth.route('/')
@auth.route('/<int:id>')
@login_required
def profile(id=None):
    if id and g.user.has_roles('admin'):
        user = User.query.get_or_404(id)
    else:
        user = g.user
    return render_template("auth/show.html", profile=user)
