from flask import g, render_template
from flask.ext.security import LoginForm, login_required


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


@auth.route('/sign_in')
def sign_in():
    return render_template('auth/sign_in.html', sign_in_form=LoginForm())
