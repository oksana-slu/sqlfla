# -*- encoding: utf-8 -*-
import os
import sys

app_path = os.path.abspath(os.path.dirname(__file__))
app_path in sys.path or sys.path.insert(0, app_path)

from flask import Flask, g, send_from_directory
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.assets import Environment
from flask.ext.babel import Babel
from flask.ext.mail import Mail
from flask.ext.security import LoginForm, RegisterForm, current_user

from .main import vendor_js, user_js
import settings


app = Flask(__name__)
app.config.from_object(settings)
app.mail = Mail(app)

db = SQLAlchemy(app)
assets = Environment(app)
babel = Babel(app)

assets.register("vendor_js", vendor_js)
assets.register("user_js", user_js)

# from core import core
from auth import auth
from events import events
from core import core

app.register_blueprint(core)
app.register_blueprint(auth, url_prefix="/profile")
app.register_blueprint(events, url_prefix="/events")


@app.before_request
def setup_env():
    g.user = current_user
    app.jinja_env.globals['sign_in_form'] = LoginForm()
    app.jinja_env.globals['sign_up_form'] = RegisterForm()


@app.route('/crossdomain.xml')
def crossdomain():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'crossdomain.xml', mimetype='text/xml')


@app.after_request
def inject_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response
