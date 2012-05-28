from flask import Blueprint, g, session


auth = Blueprint('auth', __name__, template_folder='templates')

import views
import models


@auth.before_app_request
def populate_user():
    if getattr(g, 'user', None):
        return
    elif session.get('uid'):
        g.user = models.User.query.get(session['uid'])
