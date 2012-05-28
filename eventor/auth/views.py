from flask import render_template, redirect, request, url_for, flash

from . import auth
from .forms import AuthForm
from .models import User
from .utils import login, logout


@auth.route('/', methods=['GET', 'POST'])
def sign_in():
    form = AuthForm(request.form or None)

    if request.form and form.validate():
        user = User.authenticate(form.login.data, form.password.data)
        if user is not None:
            login(user)
            return redirect(url_for('.profile'))
        else:
            flash('Authentication failed. Please, try again.', 'error')
            return redirect(url_for('.sign_in'))

    return render_template("base.html", sign_in_form=form)
    # return render_template('auth/sign_in.html', form=form)


@auth.route('/sign_out')
def sign_out():
    logout()
    return redirect(url_for('.sign_in'))


@auth.route('/profile')
@auth.route('/profile/<int:id>')
def profile(id=None):
    return render_template("auth/show.html")
