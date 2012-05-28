from flask import redirect, url_for

from . import core


@core.route("/")
def index():
    return redirect(url_for('auth.sign_in'))
